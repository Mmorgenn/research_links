from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class SearchingK:

    @staticmethod
    def searching_menu_keyboard() -> InlineKeyboardMarkup:
        random_b = InlineKeyboardButton(text="🔍 Случайный поиск", callback_data="random_searching")
        clean_history_b = InlineKeyboardButton(text="🗑 Очистить историю", callback_data="clean_history")
        menu_b = InlineKeyboardButton(text="➡️ Вернуться в меню", callback_data="main_menu")

        return InlineKeyboardMarkup(inline_keyboard=[[random_b], [clean_history_b], [menu_b]])

    @staticmethod
    def searching_keyboard(like_on: bool,
                           other_chat_id: str | None = None) -> InlineKeyboardMarkup:
        like_b = InlineKeyboardButton(text="👍", callback_data=f"like_{other_chat_id}")
        next_b = InlineKeyboardButton(text="➡️", callback_data="random_searching")
        back_b = InlineKeyboardButton(text="▶️ Обратно", callback_data="searching")

        keyboard = [[like_b, next_b], [back_b]] if like_on else [[next_b], [back_b]]

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
