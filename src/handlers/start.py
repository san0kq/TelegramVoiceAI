from __future__ import annotations

from typing import TYPE_CHECKING
from logging import getLogger

from aiogram import Router
from aiogram.filters import Command

if TYPE_CHECKING:
    from aiogram.types import Message

from filters import IsPrivateFilter
from services import create_user
from services.api_services import log_event


logger = getLogger(__name__)

router = Router()
router.message.filter(IsPrivateFilter())


@router.message(Command('start'))
async def start_handler(message: Message) -> None:
    """Handler for the /start command in private chats.

    Sends a welcome message to the user when the /start command is received.

    Args:
        message (Message): The message object representing the command.

    """
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    welcome_message = (
        'Hello! My name is J.A.R.V.I.S. I am an artificial intelligence '
        'created by Tony Stark. I am ready to assist you with any questions, '
        'but remember, I am a voice assistant, so you can only communicate '
        'with me using your voice (perhaps my new owner will add other '
        'functions someday). Also, I can determine your mood from a photo! '
        'Just send me your photo, and I will respond. You can introduce '
        'yourself right away, and I will remember your name. I look forward '
        'to starting our conversation!'
    )

    log_event(event_name='start_command', user_id=str(user_id), event_properties={'command': '/start'})

    await create_user(
        user_id=user_id,
        username=username,
        fullname=fullname
    )
    await message.answer(welcome_message)
