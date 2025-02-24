from aiogram.dispatcher.filters.state import State, StatesGroup

# Holatlar
class RegistrationState(StatesGroup):
    name = State()
    phone = State()

