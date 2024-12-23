from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class SettingK:

    @staticmethod
    def setting_keyboard() -> InlineKeyboardMarkup:
        form_b = InlineKeyboardButton(text="📝 Моя анкета", callback_data="form")
        name_b = InlineKeyboardButton(text="🙎‍♂️ Изменить имя", callback_data="name")
        age_b = InlineKeyboardButton(text="🎅 Изменить возраст", callback_data="age")
        status_b = InlineKeyboardButton(text="📊 Изменить статус", callback_data="status")
        area_b = InlineKeyboardButton(text="📚 Изменить научную область", callback_data="area")
        info_b = InlineKeyboardButton(text="📖 Изменить описание", callback_data="info")
        menu_b = InlineKeyboardButton(text="➡️ Вернуться в меню", callback_data="main_menu")

        return InlineKeyboardMarkup(
            inline_keyboard=[[form_b], [name_b], [age_b], [status_b], [area_b], [info_b], [menu_b]]
        )
