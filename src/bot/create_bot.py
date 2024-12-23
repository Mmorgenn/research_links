from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sentence_transformers import SentenceTransformer



TOKEN = "7970103613:AAEhcSW_b3_mTowE4yOe6u3hkFqMi-Vj2qg"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
model = SentenceTransformer("all-MiniLM-L6-v2")
