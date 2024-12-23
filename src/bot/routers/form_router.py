from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, User
from aiogram.filters import CommandStart
from src.bot.keyboards.form_keyboard import FormK
from src.bot.response import response
from src.bot.utils.filters import List_Filter
from src.bot.utils.questionnaire import Questionnaire
from src.bot.database import client_connect
from src.bot.create_bot import bot
from src.bot.routers.menu_router import MenuState
from src.bot.routers.states import FormState
from src.parsers.google_scholarly import GooglePars
from src.parsers.github_parser import GithubPars


form_router = Router()

POSSIBLE_GENDER = ["Мужчина", "Женщина"]
POSSIBLE_STATUS = ["Студент", "Самоучка", "Стартапер", "Работаю"]
POSSIBLE_AREA = ["Биология", "Химия", "Математика", "Физика", "It"]


@form_router.message(CommandStart())
async def start(message: Message | CallbackQuery, state: FSMContext) -> None:
    if not isinstance(message.from_user, User):
        return None

    await state.clear()
    if isinstance(message, Message):
        answer = message.answer
    elif isinstance(message.message, Message):
        answer = message.message.answer
    else:
        return None

    user_id = str(message.from_user.id)
    collection = await client_connect(user_id)
    has_user = await collection.has_user()

    if has_user:
        await answer(text=response["already_reg"])
        await state.set_state(MenuState.menu)
    else:
        await answer(text=response["gender"], reply_markup=FormK.gender_keyboard())
        await state.set_state(FormState.gender)


@form_router.callback_query(F.data == "restart")
async def restart(call: CallbackQuery, state: FSMContext) -> None:
    form = await state.get_data()
    bot_message = form.get("message")
    if isinstance(bot_message, Message):
        await bot.delete_message(bot_message.chat.id, bot_message.message_id)
    await state.clear()
    await state.set_state(FormState.gender)
    if isinstance(call.message, Message):
        await call.message.answer(text=response["restart"], reply_markup=FormK.gender_keyboard())


@form_router.message(FormState.gender, lambda message: message.text.title() in POSSIBLE_GENDER)
async def get_gender_message(message: Message, state: FSMContext) -> None:
    await state.update_data(gender=str(message.text).title())
    await state.set_state(FormState.name)

    if not isinstance(message.from_user, User):
        return None
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    await message.answer(text=response["name"], reply_markup=FormK.name_keyboard(
                         f"{first_name} {last_name if last_name else ""}"))


@form_router.message(FormState.name)
async def get_name_message(message: Message, state: FSMContext) -> None:
    await state.update_data(name=str(message.text).title())
    await state.set_state(FormState.age)
    await message.answer(text=response["age"].format(message.text))


@form_router.message(FormState.age, lambda message: message.text.isdigit())
async def get_age_message(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await state.set_state(FormState.status)
    await message.answer(text=response["status"], reply_markup=FormK.status_keyboard())


@form_router.message(FormState.status, lambda message: message.text.title() in POSSIBLE_STATUS)
async  def get_status_message(message: Message, state: FSMContext) -> None:
    await state.update_data(status=str(message.text).title())
    await state.set_state(FormState.area)
    await message.answer(text=response["area"], reply_markup=FormK.area_keyboard())


@form_router.message(FormState.area, List_Filter(POSSIBLE_AREA))
async def get_area_message(message: Message, state: FSMContext) -> None:
    await state.update_data(area=str(message.text).title())
    await state.set_state(FormState.info)
    await message.answer(text=response["info"])


@form_router.message(FormState.info)
async def start_integration(message: Message, state: FSMContext) -> None:
    await state.update_data(info=message.text)
    await state.set_state(FormState.integration)
    await message.answer(text=response["integration"], reply_markup=FormK.integration_keyboard())


@form_router.callback_query(FormState.integration, F.data == "gscholar")
async def ask_gscholar(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        return None

    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(FormState.gscholar)
    await call.message.answer(text=response["gscholar"])


@form_router.callback_query(FormState.integration, F.data == "github")
async def ask_github(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        return None

    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(FormState.github)
    await call.message.answer(text=response["github"])


@form_router.message(FormState.gscholar)
async def get_scholar(message: Message, state: FSMContext) -> None:
    result = GooglePars(str(message.text)).get_info()
    if not result:
        await message.answer(text=response["repeat"])
        return None

    await state.update_data(result)
    await state.set_state(FormState.integration)
    await message.answer(text=response["integration"], reply_markup=FormK.integration_keyboard())


@form_router.message(FormState.github)
async def get_github(message: Message, state: FSMContext) -> None:
    result = GithubPars(str(message.text)).get_info()
    if not result:
        await message.answer(text=response["repeat"])
        return None

    await state.update_data(result)
    await state.set_state(FormState.integration)
    await message.answer(text=response["integration"], reply_markup=FormK.integration_keyboard())


@form_router.callback_query(FormState.integration, F.data == "finish")
async def get_info_message(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        return None

    form_data = await state.get_data()
    form = Questionnaire(form_data).show()
    bot_message = await call.message.answer(text=response["permission"].format(form),
                                            reply_markup=FormK.final_keyboard())
    await state.update_data(message=bot_message)


@form_router.callback_query(F.data == "upload")
async def upload_questionnaire(call: CallbackQuery, state: FSMContext) -> None:
    if not (isinstance(call.from_user, User) and isinstance(call.message, Message)):
        return None

    user_id = str(call.from_user.id)
    form = await state.get_data()
    bot_message = form.pop("message")
    if "gscholar" in form.keys():
        gscholar = form["gscholar"]
        form.update(gscholar)

    if "github" in form.keys():
        github = form["github"]
        form.update(github)

    collection = await client_connect(user_id)
    await collection.add_user(form, str(call.from_user.username), str(call.message.chat.id))

    if isinstance(bot_message, Message):
        await bot.delete_message(bot_message.chat.id, bot_message.message_id)

    await state.clear()
    await state.set_state(MenuState.menu)
    await call.message.answer(text=response["login"])
