from uuid import uuid4
from pathlib import Path
from typing import BinaryIO, Optional
from logging import getLogger

from openai import AsyncOpenAI

from config import settings
from data_access.redis import async_redis_client
from data_access.dal import AsyncRedisThreadsDAL
from services.exceptions import (
    VoiceToTextError,
    GetResponseError,
    TextToVoiceError
)


logger = getLogger(__name__)

openai_client = AsyncOpenAI(
    api_key=settings.openai_api_key,
)

async def voice_to_text(voice_file: BinaryIO) -> Optional[str]:
    """Converts voice file to text using OpenAI API.

    Args:
        voice_file (BinaryIO): The voice file to be converted.

    Returns:
        Optional[str]: The transcribed text if successful, otherwise None.

    Raises:
        VoiceToTextError: If an error occurs during conversion.

    """
    voice_file.name = 'voice.oga'
    try:
        transcription = await openai_client.audio.transcriptions.create(
            model='whisper-1', 
            file=voice_file,
            response_format='text'
        )
        logger.info(
            'Voice-to-text conversion completed successfully. Text: %s',
            transcription
        )
        return transcription
    except Exception as e:
        logger.error('Error converting voice to text - %s', e)
        raise VoiceToTextError(
            'Error converting voice to text'
        )


async def get_answer(text: str, user_id: int) -> Optional[str]:
    """Get response from OpenAI API based on user's text.

    Args:
        text (str): The text message from the user.
        user_id (int): The ID of the user sending the message.

    Returns:
        Optional[str]: The response from the OpenAI API if successful,
        otherwise None.

    Raises:
        GetResponseError: If an error occurs during the retrieval of response.

    """
    try:
        async with async_redis_client as client:
            redis_dal = AsyncRedisThreadsDAL(redis_client=client)

            if not await redis_dal.check_exists(user_id=user_id):
                '''
                if the user is not in the database,
                it means we create a new thread with them
                '''
                empty_thread = await openai_client.beta.threads.create()
                await redis_dal.create_thread(
                    user_id=user_id,
                    thread_id=empty_thread.id
                )
                thread_id = empty_thread.id
                await openai_client.beta.threads.messages.create(
                    thread_id=thread_id,
                    role='user',
                    content=text
                )
            else:
                '''
                if the user is in the database, it means they have already
                interacted with AI, and we retrieve an existing thread to
                continue the conversation
                '''
                thread_id = await redis_dal.get_thread(user_id=user_id)
                thread_id = thread_id.decode('utf-8')
                await openai_client.beta.threads.messages.create(
                    thread_id=thread_id,
                    role='user',
                    content=text
                )
            
            await openai_client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=settings.assistant_id
            )
            

            thread_messages = await openai_client.beta.threads.messages.list(
                thread_id=thread_id
            )

            last_message = await openai_client.beta.threads.messages.retrieve(
                message_id=thread_messages.first_id,
                thread_id=thread_id,
                )
            
            text = last_message.content[0].text.value
            logger.info('Response received. User: %s, Text: %s', user_id, text)
            return text
    
    except Exception as e:
        logger.error('Error receiving response - %s', e)
        raise GetResponseError('Error receiving response')


async def text_to_voice(text: str) -> Optional[str]:
    """Converts text to voice using OpenAI API.

    Args:
        text (str): The text to be converted.

    Returns:
        Optional[str]: The path to the generated voice file if successful,
        otherwise None.

    Raises:
        TextToVoiceError: If an error occurs during conversion.

    """
    try:
        speech_file_path = Path(__file__).parent / 'temp_audio' / f'{uuid4()}.mp3'
        response = await openai_client.audio.speech.create(
            model='tts-1',
            voice='echo',
            input=text
        )
        response.write_to_file(speech_file_path)

        logger.info('Audio successfully created. Path: %s', speech_file_path)
        return speech_file_path
    
    except Exception as e:
        logger.error('Error converting text to voice - %s', e)
        raise TextToVoiceError('Error converting text to voice')
