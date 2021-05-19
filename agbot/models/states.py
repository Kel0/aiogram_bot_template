from aiogram.dispatcher.filters.state import State, StatesGroup


class UseState(StatesGroup):
    who = State()
