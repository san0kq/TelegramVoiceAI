import logging
import sys
from contextlib import asynccontextmanager
import uvicorn
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from handlers import register_routes

logger = logging.getLogger(__name__)

WEBHOOK_PATH = f'/bot/{settings.tg_token}'
WEBHOOK_URL = settings.webhook_url + WEBHOOK_PATH


storage = MemoryStorage()

bot = Bot(token=settings.tg_token)
dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    await bot.set_webhook(url=WEBHOOK_URL)

    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)

register_routes(dp)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict) -> None:
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-1s [%(asctime)s] - %(name)s - %(message)s',
        handlers=(logging.StreamHandler(sys.stdout), logging.FileHandler('file.log'))
    )

    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
