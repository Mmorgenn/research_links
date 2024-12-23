from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User

from src.bot.database import client_connect
from src.bot.keyboards import FormK, MenuK, SettingK
from src.bot.response import response
from src.bot.routers.form_router import POSSIBLE_AREA, POSSIBLE_STATUS
from src.bot.routers.menu_router import delete_message
from src.bot.routers.states import MenuState, SettingState
from src.bot.utils.filters import List_Filter
from src.bot.utils.questionnaire import Questionnaire

setting_router = Router()
keyboards = {"status": FormK.status_keyboard(), "area": FormK.area_keyboard()}
FORMS = ["name", "age", "info", "status", "area", "info"]


@setting_router.callback_query(MenuState.menu, F.data == "setting")
async def settings(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        return None
    await delete_message(call.message)
    await call.message.answer(text="Выбери что изменить в акнете:", reply_markup=SettingK.setting_keyboard())


@setting_router.callback_query(MenuState.menu, F.data == "form")
async def show_form(call: CallbackQuery, state: FSMContext) -> None:
    if not (isinstance(call.message, Message) and isinstance(call.from_user, User)):
        return None

    await delete_message(call.message)
    user_id = str(call.from_user.id)
    collection = await client_connect(user_id)
    metadatas = await collection.get_self_form()
    if not bool(metadatas):
        await state.clear()
        await call.message.answer(text=response["not_found"])
    else:
        await call.message.answer(text=Questionnaire(metadatas).show(), reply_markup=MenuK.back_keyboard("setting"))


@setting_router.callback_query(MenuState.menu, lambda x: x.data in FORMS)
async def request_change(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        return None

    form = str(call.data)
    await delete_message(call.message)
    await call.message.answer(text=response.get(f"new_{form}", "Ошибка! /menu"), reply_markup=keyboards.get(form))
    await state.set_state(getattr(SettingState, form))


async def confirm_change(message: Message, state: FSMContext) -> None:
    if not isinstance(message.from_user, User):
        return None

    user_id = str(message.from_user.id)
    form = await state.get_state()
    form = str(form).split(":")[1]
    new_value = str(message.text).title() if form != "info" else str(message.text)
    collection = await client_connect(user_id)
    await collection.update_form(form, new_value)

    await state.set_state(MenuState.menu)
    bot_message = await message.answer(text=response["change"], reply_markup=MenuK.back_keyboard("setting"))
    await state.update_data(previous_message=bot_message)


setting_router.message.register(confirm_change, SettingState.name)
setting_router.message.register(confirm_change, SettingState.age, lambda message: message.text.isdigit())
setting_router.message.register(
    confirm_change, SettingState.status, lambda message: message.text.title() in POSSIBLE_STATUS
)
setting_router.message.register(confirm_change, SettingState.area, List_Filter(POSSIBLE_AREA))
setting_router.message.register(confirm_change, SettingState.info)
