import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from config import settings
from handlers import register_routes
from data_access.redis import async_redis_client

logger = logging.getLogger(__name__)


storage = RedisStorage(
    redis=async_redis_client,
)

bot = Bot(token=settings.tg_token)
dp = Dispatcher(storage=storage)


register_routes(dp)


async def main() -> None:
    bot = Bot(token=settings.tg_token)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-1s [%(asctime)s] - %(name)s - %(message)s',
        handlers=(logging.StreamHandler(sys.stdout), logging.FileHandler('file.log'))
    )

    asyncio.run(main())
