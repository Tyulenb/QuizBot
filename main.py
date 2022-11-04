from config import types, bot, dp, executor, adminid
from QuizCreation import *
from SolveQuiz import *
from commands import *


async def on_start(i):
    await bot.send_message(adminid, text="Started\n/start")


async def on_shutdown(i):
    await bot.send_message(adminid, text="Ended")


reg_QuizCreation_handlers(dp)
reg_SolveQuiz_handlers(dp)
reg_commands_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_start, on_shutdown=on_shutdown, skip_updates=True)
