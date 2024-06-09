from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    thread_id = State()
