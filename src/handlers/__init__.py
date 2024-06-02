from aiogram import Dispatcher
from .start import router as start_routes
from .voice import router as voice_routes


def register_routes(dp: Dispatcher):
    dp.include_router(start_routes)
    dp.include_router(voice_routes)
