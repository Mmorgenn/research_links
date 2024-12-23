from aiogram.filters.state import State, StatesGroup


class FormState(StatesGroup):
    name = State()
    gender = State()
    age = State()
    status = State()
    area = State()
    info = State()
    integration = State()
    github = State()
    gscholar = State()


class MenuState(StatesGroup):
    menu = State()


class SettingState(StatesGroup):
    name = State()
    gender = State()
    age = State()
    status = State()
    area = State()
    info = State()
