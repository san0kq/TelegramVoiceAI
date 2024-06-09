from __future__ import annotations

import os
from typing import TYPE_CHECKING
from logging import getLogger

from aiogram import Router, F

if TYPE_CHECKING:
    from aiogram.types import Message


from filters import IsPrivateFilter
from config import settings
from services import get_mood_by_photo
from services.api_services import log_event


logger = getLogger(__name__)

router = Router()
router.message.filter(IsPrivateFilter())

@router.message(F.content_type == 'photo')
async def handle_photo_message(message: Message) -> None:
    """Handle messages that are not voice messages in private chats.

    Sends a message to inform the user that only voice messages are accepted.

    Args:
        message (Message): The message received.

    """
    user_id = message.from_user.id
    photo_id = message.photo[-1].file_id

    wait_message = await message.answer(text='💬')

    photo = await message.bot.get_file(file_id=photo_id)
    photo_url = f'https://api.telegram.org/file/bot{settings.tg_token}/{photo.file_path}'
    mood = await get_mood_by_photo(photo_url=photo_url)

    if mood != '0':
        await message.answer(text=f'Your mood: {mood}.')

        log_event(
            event_name='check_mood',
            user_id=str(user_id), 
            event_properties={'mood': mood}
        )
    else:
        await message.answer(
            text="Sorry, I couldn't determine your mood from this photo. Try again, please."
        )
        log_event(
            event_name='check_mood',
            user_id=str(user_id), 
            event_properties={'mood': 'not determined'}
        )

    await wait_message.delete()
