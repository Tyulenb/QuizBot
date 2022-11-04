from config import types, Dispatcher
from dtbase import *
from keyboards import *


async def start(message: types.Message):
    await message.answer(text="Для того чтобы начать воспользуйтесь кнопками", reply_markup=Start_Markup)
    await Enter_User_Id(message.from_user.id)


async def get_user_info(message: types.Message):
    stats = await Get_User_Stats(message.from_user.id)
    Percentage = await Get_User_Percentage(message.from_user.id)
    if(stats[0]==None):
        QuizCompleted=0
    else:
        QuizCompleted = stats[0]
    if(stats[1]==None):
        AmountOfAnsw=0
    else:
        AmountOfAnsw=stats[1]
    if(stats[3]==None):
        QuizCreated=0
    else:
        QuizCreated = stats[3]
    answer = f"{message.from_user.first_name}\nВикторин пройдено: {QuizCompleted}\n"\
    f"Процент правильных ответов: {Percentage}\nВсего ответов: {AmountOfAnsw}\nВикторин создано: {QuizCreated}"
    await message.answer(text=answer)


def reg_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(get_user_info, commands="stats", state="*")