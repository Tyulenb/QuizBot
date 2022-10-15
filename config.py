from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from token import tok, adminid
token = tok # наш токен
adminid = adminid # ваш id
storage = MemoryStorage()
bot = Bot(token)
dp = Dispatcher(bot, storage=storage)