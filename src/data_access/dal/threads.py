from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from logging import getLogger

if TYPE_CHECKING:
    from redis.asyncio import Redis

from data_access.exceptions import ThreadNotExistsError, AddThreadError


logger = getLogger(__name__)


class AsyncRedisThreadsDAL:
    """Data Access Layer for managing threads in Redis asynchronously.

    Args:
        redis_client (Redis): A Redis client instance.

    Attributes:
        redis_client (Redis): A Redis client instance used for database
        operations.

    Raises:
        ThreadNotExistsError: If the thread for the specified user does not
        exist.
        AddThreadError: If there is an error while adding a new thread to
        Redis.

    """
    def __init__(self, redis_client: Redis) -> None:
        """Initialize the AsyncRedisThreadsDAL instance with a Redis client."""
        self.redis_client = redis_client

    async def check_exists(self, user_id: int) -> bool:
        """Check if a thread exists for the specified user.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the thread exists, False otherwise.

        """
        return await self.redis_client.exists(user_id)

    async def get_thread(self, user_id: int) -> Optional[str]:
        """Retrieve the thread ID associated with the specified user.

        Args:
            user_id (int): The ID of the user to retrieve the thread for.

        Returns:
            Optional[str]: The thread ID if it exists, otherwise None.

        Raises:
            ThreadNotExistsError: If the thread for the specified user does
            not exist.

        """
        if await self.check_exists(user_id):
            return await self.redis_client.get(user_id)
        else:
            raise ThreadNotExistsError(
                'Thread of user %s does not exist', user_id
            )

    async def create_thread(
            self,
            user_id: int,
            thread_id: str
    ) -> Optional[str]:
        """Create a new thread for the specified user and store it in Redis.

        Args:
            user_id (int): The ID of the user to create the thread for.
            thread_id (str): The ID of the thread to store.

        Returns:
            Optional[str]: The ID of the created thread.

        Raises:
            AddThreadError: If there is an error while adding the new
            thread to Redis.

        """
        try:
            await self.redis_client.set(user_id, thread_id)
        except Exception as err:
            logger.exception(
                '[!x!] Failed storing thread in Redis: user_id - "%s", thread_id - "%s". Exception: %s',
                user_id,
                thread_id,
                err,
            )
            raise AddThreadError(
                'Error adding new Thread (%s) for user %s', thread_id, user_id
            )
        return thread_id
