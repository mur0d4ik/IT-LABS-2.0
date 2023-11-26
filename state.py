from aiogram.dispatcher.filters.state import StatesGroup, State


class cours(StatesGroup):

    name = State()
    age = State()
    courses = State()
    phone_number = State()


    check = State()