from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, User
from src.bot.routers.states import MenuState
from src.bot.routers.menu_router import delete_message, send_other_chat
from src.bot.keyboards import MenuK, SearchingK, CoworkerK
from src.bot.response import response
from src.bot.database import client_connect
from src.bot.utils.questionnaire import Questionnaire


searching_router = Router()


@searching_router.callback_query(MenuState.menu, F.data == "searching")
async def searching_menu(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        return

    await delete_message(call.message)
    await call.message.answer(text="Меню поиска", reply_markup=SearchingK.searching_menu_keyboard())


@searching_router.callback_query(MenuState.menu, F.data == "clean_history")
async def clean_history(call: CallbackQuery) -> None:
    if not (isinstance(call.message, Message) and isinstance(call.from_user, User)):
        return None

    await delete_message(call.message)
    user_id = str(call.from_user.id)
    collection = await client_connect(user_id)
    await collection.clean_viewed()
    await call.message.answer(text=response["clean"], reply_markup=MenuK.back_keyboard("searching"))


@searching_router.callback_query(MenuState.menu, F.data == "random_searching")
async def random_searching(call: CallbackQuery) -> None:
    if not (isinstance(call.message, Message) and isinstance(call.from_user, User)):
        return None

    await delete_message(call.message)
    user_id = str(call.from_user.id)
    collection = await client_connect(user_id)
    result = await collection.get_similar_form()

    if not result:
        await call.message.answer(text=response["searching_stop"], reply_markup=MenuK.back_keyboard("searching"))
    else:
        form, chat_id = result
        await call.message.answer(text=Questionnaire(form).show(),
                                  reply_markup=SearchingK.searching_keyboard(True, chat_id))


@searching_router.callback_query(MenuState.menu, lambda cb: cb.data and cb.data.startswith("like"))
async def random_like(call: CallbackQuery) -> None:
    if not (isinstance(call.message, Message) and isinstance(call.from_user, User)):
        return None

    await delete_message(call.message)
    user_id = str(call.from_user.id)
    chat_id = str(call.data).split("_")[1]
    if chat_id:
        collection = await client_connect(user_id)
        form = await collection.get_self_form()
        await send_other_chat(chat_id, text=Questionnaire(form).show(response["notification"]),
                              markup=CoworkerK.notification_keyboard(
                              user_id, str(call.from_user.username), str(call.message.chat.id)))
    await call.message.answer(text=str(call.message.text),
                              reply_markup=SearchingK.searching_keyboard(False))

