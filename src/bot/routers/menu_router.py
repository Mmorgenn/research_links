from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from src.bot.create_bot import bot
from src.bot.keyboards import MenuK
from src.bot.routers.states import MenuState

menu_router = Router()


async def delete_message(message: Message) -> None:
    await bot.delete_message(message.chat.id, message.message_id)


async def send_other_chat(chat_id: str, text: str, markup: InlineKeyboardMarkup | None = None) -> None:
    await bot.send_message(chat_id, text, reply_markup=markup)


async def main_menu(message: Message | CallbackQuery) -> None:
    if isinstance(message, CallbackQuery) and isinstance(message.message, Message):
        message = message.message
        await delete_message(message)
    await message.answer(text="<b>Главное Меню</b>", reply_markup=MenuK.menu_keyboard())


menu_router.message.register(main_menu, MenuState.menu, Command("menu"))
menu_router.callback_query.register(main_menu, MenuState.menu, F.data == "main_menu")
