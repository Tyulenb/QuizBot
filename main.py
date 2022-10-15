from config import types, bot, dp, executor, adminid, InlineKeyboardMarkup, InlineKeyboardButton
from QuizCreation import *


async def on_start(i):
    await bot.send_message(adminid, text="Started", reply_markup=NewQuizButt)


async def on_shutdown(i):
    await bot.send_message(adminid, text="Ended")


reg_QuizCreation_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_start, on_shutdown=on_shutdown, skip_updates=True)
