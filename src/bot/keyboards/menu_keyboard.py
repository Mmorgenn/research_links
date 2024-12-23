from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class MenuK:

    @staticmethod
    def menu_keyboard() -> InlineKeyboardMarkup:

        setting_b = InlineKeyboardButton(text="⚙️ Настройки", callback_data="setting")
        searching_b = InlineKeyboardButton(text="🔍 Поиск коллег", callback_data="searching")
        coworker_b = InlineKeyboardButton(text="🗣 Коллеги", callback_data="coworker_0")

        return InlineKeyboardMarkup(inline_keyboard=[[coworker_b, searching_b], [setting_b]])

    @staticmethod
    def back_keyboard(callback_data: str | None = None) -> InlineKeyboardMarkup:
        menu_b = InlineKeyboardButton(text="➡️ Вернуться в меню", callback_data="main_menu")
        keyboard = [[menu_b]]

        if callback_data:
            back_b = InlineKeyboardButton(text="▶️ Обратно", callback_data=callback_data)
            keyboard[0].insert(0, back_b)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
