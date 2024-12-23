from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class CoworkerK:

    @staticmethod
    def notification_keyboard(user_id: str, username: str, chat_id: str) -> InlineKeyboardMarkup:
        like_b = InlineKeyboardButton(text="👍", callback_data=f"reply_like_{user_id}_{chat_id}")
        dislike_b = InlineKeyboardButton(text="👎", callback_data="reply_dislike")
        connect_b = InlineKeyboardButton(text="📝 Написать", url=f"https://t.me/{username}")

        return InlineKeyboardMarkup(inline_keyboard=[[like_b, dislike_b], [connect_b]])

    @staticmethod
    def coworker_keyboard(username: str, ind: int) -> InlineKeyboardMarkup:
        left_b = InlineKeyboardButton(text="⬅️", callback_data=f"coworker_{ind - 1}")
        right_b = InlineKeyboardButton(text="➡️", callback_data=f"coworker_{ind + 1}")
        connect_b = InlineKeyboardButton(text="📝 Написать", url=f"https://t.me/{username}")
        menu_b = InlineKeyboardButton(text="▶️ Вернуться в меню", callback_data="main_menu")

        return InlineKeyboardMarkup(inline_keyboard=[[left_b, right_b], [menu_b], [connect_b]])
