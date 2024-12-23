from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


class FormK:

    @staticmethod
    def gender_keyboard() -> ReplyKeyboardMarkup:

        male_b = KeyboardButton(text="Мужчина")
        female_b = KeyboardButton(text="Женщина")

        return ReplyKeyboardMarkup(keyboard=[[male_b, female_b]], resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def name_keyboard(user_name: str) -> ReplyKeyboardMarkup:
        user_b = KeyboardButton(text=user_name)

        return ReplyKeyboardMarkup(keyboard=[[user_b]], resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def status_keyboard() -> ReplyKeyboardMarkup:

        student_b = KeyboardButton(text="Студент")
        staught_b = KeyboardButton(text="Самоучка")
        startup_b = KeyboardButton(text="Стартапер")
        worker_b = KeyboardButton(text="Работаю")

        return ReplyKeyboardMarkup(keyboard=[[student_b, staught_b], [startup_b, worker_b]],
                                   resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def area_keyboard() -> ReplyKeyboardMarkup:

        biology_b = KeyboardButton(text="Биология")
        chemistry_b = KeyboardButton(text="Химия")
        physic_b = KeyboardButton(text="Физика")
        math_b = KeyboardButton(text="Математика")
        it_b = KeyboardButton(text="IT")

        return ReplyKeyboardMarkup(keyboard=[[biology_b, chemistry_b], [physic_b, math_b], [it_b]],
                                   resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def integration_keyboard() -> InlineKeyboardMarkup | None:

        github_b = InlineKeyboardButton(text="GitHub", callback_data="github")
        gscholar_b = InlineKeyboardButton(text="Google Scholar", callback_data="gscholar")
        next_b = InlineKeyboardButton(text="Дальше", callback_data="finish")

        return InlineKeyboardMarkup(inline_keyboard=[[github_b, gscholar_b], [next_b]])

    @staticmethod
    def final_keyboard() -> InlineKeyboardMarkup:

        agree_b = InlineKeyboardButton(text="✅", callback_data="upload")
        disagree_b = InlineKeyboardButton(text="⛔️", callback_data="restart")

        return InlineKeyboardMarkup(inline_keyboard=[[agree_b, disagree_b]])
