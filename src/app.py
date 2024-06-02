import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from handlers import register_routes

logger = logging.getLogger(__name__)


storage = MemoryStorage()

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
