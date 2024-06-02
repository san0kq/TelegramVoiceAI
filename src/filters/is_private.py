from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.filters import BaseFilter

if TYPE_CHECKING:
    from aiogram.types import Message


class IsPrivateFilter(BaseFilter):
    """Filter to check if the message is sent in a private chat."""
    async def __call__(self, obj: Message) -> bool:
        """Check if the message is sent in a private chat.

        Args:
            obj (Message): The message to check.

        Returns:
            bool: True if the message is sent in a private chat, False
            otherwise.

        """
        return obj.chat.type == 'private'
