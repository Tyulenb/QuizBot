from config import types, Dispatcher, StatesGroup, State, FSMContext
from dtbase import *
from keyboards import *
import random

#присылает список всех викторин
async def show_list(callback: types.CallbackQuery):
    s = await Quiz_list()
    await callback.message.answer(s, reply_markup=SolveQuiz_NewQuiz_Markup)

class QSolving(StatesGroup):
    solving = State()

async def start_solving(callback: types.CallbackQuery):
    await QSolving.solving.set()
    await callback.message.answer("Введите id викторины")


# реакция на верный ответ в викторине
async def RightAnsw(callback: types.CallbackQuery, state: FSMContext):
    global answer_сounter, right_answers_counter, UserID
    answer_сounter += 1
    right_answers_counter += 1

    if answer_сounter == len(arr_of_questions):
        await callback.message.answer("\U0001F4AC Вы прошли викторину! \U0001F4AC\n"
        f"Вы ответили {right_answers_counter}\{len(arr_of_questions)} правильно!", reply_markup=Show_correct_Answ_Markup)
        await state.finish()
        await Enter_User_AmountOfAnsw(UserID, len(arr_of_questions)) # добавление количества ответов в статистику пользователя
        await Enter_User_Ransw(UserID, right_answers_counter) # добавление количества правильных ответов в статистику пользователя
        await Enter_User_QuizCompleted(UserID)

    s="Вы ответили верно! \U00002705"
    await callback.message.edit_text(text=s)


# реакция на неверный ответ в вкиторине
async def WrongAnsw(callback: types.CallbackQuery, state: FSMContext):
    global answer_сounter, UserID
    answer_сounter += 1

    if answer_сounter == len(arr_of_questions):
        await callback.message.answer("\U0001F4AC Вы прошли викторину! \U0001F4AC \n"
        f"Вы ответили {right_answers_counter}\{len(arr_of_questions)} правильно!", reply_markup=Show_correct_Answ_Markup)
        await state.finish()
        await Enter_User_AmountOfAnsw(UserID, len(arr_of_questions))
        await Enter_User_Ransw(UserID, right_answers_counter)
        await Enter_User_QuizCompleted(UserID)

    s="Вы ответили неверно! \U0000274C"
    await callback.message.edit_text(text=s)


#метод который за все отвечает
async def solve(message: types.Message, state: FSMContext):

    global arr_of_questions # массив со вопросами и ответами
    global answer_сounter # счетчик ответов
    global right_answers_counter # счетчик правильных ответов
    global UserID 
    right_answers_counter = 0
    answer_сounter = 0

    arr_of_questions = await Get_quest(message.text) #массив всех вопросов викторины
    if arr_of_questions == []: # проверка на корректность введенных данных
        await message.answer("Введите корректное id, используя цифры, воспользуйтесь списком", reply_markup=QuizList_Markup)
        await QSolving.solving.set()
    else:
        UserID = message.from_user.id
        Name = await Get_Quiz_Name(message.text)
        
        await message.answer(f"Викторина {Name} :")

        for i in range(len(arr_of_questions)):
            Wrl2 = False # флаги для добавления доп. неверных вариантов ответа если они существуют 
            Wrl3 = False 
            Right = InlineKeyboardButton(text=arr_of_questions[i][1], callback_data="right") # верный вариант ответа
            Wrong = InlineKeyboardButton(text=arr_of_questions[i][2], callback_data="wrong") # неверный вариант ответа
            if(arr_of_questions[i][3] != None): # проверк на наличие доп. варинат ответа
                Wrl2=True
                Wrong2 = InlineKeyboardButton(text=arr_of_questions[i][3], callback_data="wrong") # доп. неверный вариант ответа
                if(arr_of_questions[i][4] != None): # проверк на наличие доп. варинат ответа
                    Wrl3 = True
                    Wrong3 = InlineKeyboardButton(text=arr_of_questions[i][4], callback_data="wrong") # доп. неверный вариант ответа

            answers = [] # список кнопок, для того чтобы перемешать кнопки и засунуть в разметку
            answers.append(Right)
            answers.append(Wrong)
            if Wrl2: # если доп. неверный вариант ответа существует
                answers.append(Wrong2)
            if Wrl3: # если доп. неверный вариант ответа существует
                answers.append(Wrong3) 
            random.shuffle(answers)

            Var_of_Answ = InlineKeyboardMarkup(row_width=2) #разметка кнопок с вариантами ответов

            for j in range(len(answers)): #наполнение разметки с вариантами ответов кнопками из перемешенного списка
                Var_of_Answ.add(answers[j])
            await message.answer(arr_of_questions[i][0], reply_markup= Var_of_Answ)
    

async def correct_answers(callback: types.CallbackQuery):
    global arr_of_questions
    for i in range(len(arr_of_questions)):
        answer = arr_of_questions[i][0] + "\n" + "\U00002705 " + arr_of_questions[i][1] + " \U00002705"
        await callback.message.answer(text=answer)


async def Cancel_Quiz(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Отменено",reply_markup=Start_Markup)
    await state.finish()



def reg_SolveQuiz_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_list, text="list", state="*")
    dp.register_callback_query_handler(start_solving, text="Solve", state="*")
    dp.register_message_handler(solve, state=QSolving.solving)
    dp.register_callback_query_handler(RightAnsw, text="right", state=QSolving.solving)
    dp.register_callback_query_handler(WrongAnsw, text="wrong", state=QSolving.solving)
    dp.register_callback_query_handler(correct_answers, text="Show_Correct_Answers", state="*")
    dp.register_callback_query_handler(Cancel_Quiz, text="Cancel", state=QSolving.solving)
    