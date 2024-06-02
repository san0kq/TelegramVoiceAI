from __future__ import annotations

import os
from typing import TYPE_CHECKING
from logging import getLogger

from aiogram import Router, F
from aiogram.types import FSInputFile

if TYPE_CHECKING:
    from aiogram.types import Message


from filters import IsPrivateFilter
from services import voice_to_text, get_answer, text_to_voice


logger = getLogger(__name__)

router = Router()
router.message.filter(IsPrivateFilter())


@router.message(F.content_type == 'voice')
async def handle_voice_message(message: Message) -> None:
    """Handle voice messages received in private chats.

    Converts the voice message to text, processes it to generate a response,
    converts the response to a voice message, and sends it back to the user.

    Args:
        message (Message): The voice message received.

    """
    try:
        user_id = message.from_user.id

        wait_message = await message.answer(
            text='💬'
        )
        voice_id = message.voice.file_id
        voice_object = await message.bot.get_file(file_id=voice_id)
        voice_file = await message.bot.download_file(voice_object.file_path)

        voice_text = await voice_to_text(voice_file=voice_file)

        answer = await get_answer(text=voice_text, user_id=user_id)

        voice_answer_path = await text_to_voice(text=answer)
        voice_answer = FSInputFile(voice_answer_path)

        await message.bot.send_voice(
            chat_id=user_id,
            voice=voice_answer
        )

        logger.info(
            'Response sent to the user. User ID: %s',
            user_id
        )

        await wait_message.delete()

        os.remove(voice_answer_path)  # delete voice file
        logger.info('Voice file deleted. Path: %s', voice_answer_path)
    
    except Exception as e:
        logger.error('Error! - %s', e)

        await message.answer(
            text=(
                '😬 Unfortunately, an unexpected error occurred. Please try '
                'again later or contact support at sanromanov94@gmail.com.'
            )
        )


@router.message(F.content_type != 'voice')
async def handle_not_voice_message(message: Message) -> None:
    """Handle messages that are not voice messages in private chats.

    Sends a message to inform the user that only voice messages are accepted.

    Args:
        message (Message): The message received.

    """
    await message.answer(
        text=(
            'I am a voice assistant and at the moment I can only communicate '
            'through voice messages. Please record a voice message for me.'
        )
    )
