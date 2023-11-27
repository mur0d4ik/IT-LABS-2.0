from aiogram.dispatcher.filters.state import StatesGroup, State


class cours(StatesGroup):

    name = State()
    age = State()
    courses = State()
    phone_number = State()


    check = State()



class coursADD(StatesGroup):

    cours_name = State()
    cours_time = State()
    cours_duration = State()
    cours_discription = State()
    cours_price = State()
    cours_photo = State()

    