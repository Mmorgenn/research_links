from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, User
from src.bot.keyboards import MenuK, CoworkerK
from src.bot.response import response
from src.bot.database import client_connect
from src.bot.routers.menu_router import delete_message, send_other_chat
from src.bot.utils.questionnaire import Questionnaire
from src.bot.routers.states import MenuState


coworker_router = Router()


@coworker_router.callback_query(MenuState.menu, F.data == "reply_dislike")
async def reply_dislike(call: CallbackQuery) -> None:
    if isinstance(call.message, Message):
        await delete_message(call.message)


@coworker_router.callback_query(MenuState.menu, lambda cb: cb.data and cb.data.startswith("reply_like"))
async def reply_like(call: CallbackQuery) -> None:
    if isinstance(call.message, Message):
        await delete_message(call.message)
    if not isinstance(call.from_user, User):
        return None

    user_id = str(call.from_user.id)
    data = str(call.data).split("_")
    if len(data) < 4:
        return None
    other_id = data[2]
    chat_id = data[3]
    collection = await client_connect(user_id)
    await collection.match(other_id)

    await send_other_chat(chat_id, text=response["matched"].format(call.from_user.username),
                          markup=MenuK.back_keyboard())
    await call.answer(text=response["matched_call"])


@coworker_router.callback_query(MenuState.menu, lambda cb: cb.data and cb.data.startswith("coworker"))
async def show_coworker(call: CallbackQuery) -> None:
    if not(isinstance(call.message, Message) and isinstance(call.from_user, User)):
        return None

    await delete_message(call.message)
    user_id = str(call.from_user.id)
    ind = int(str(call.data).split("_")[1])
    collection = await client_connect(user_id)

    form = await collection.get_matched(ind)
    if not form:
        await call.message.answer(text=response["no_matched"], reply_markup=MenuK.back_keyboard())
    else:
        username = form.get("username", "durov")
        await call.message.answer(text=Questionnaire(form).show(), reply_markup=CoworkerK.coworker_keyboard(username, ind))
