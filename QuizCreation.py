from config import types, Dispatcher, StatesGroup, State, FSMContext
from dtbase import *
from keyboards import *

class QCreation(StatesGroup):
    name = State()
    question = State()
    RightAnsw = State()
    WrongAnsw = State()


async def add_quiz(callback: types.CallbackQuery):
    await callback.message.answer("Введите название викторины")
    await QCreation.name.set()


#handler(name)
async def enter_quiz_name(message: types.Message):
    global flag, ID, NAME
    flag = False
    NAME = str(message.text)
    await add_quiz_name(NAME) # имя с помощью метода передается в бд
    ID = await add_question_id(NAME) # с помощью метода по имени викторины вопросу присваивается ID и сохраняется в пер
    await QCreation.question.set()
    await message.answer("Введите вопрос")


#handler(question)
async def enter_question(message: types.Message):
    global flag, NAME, ID
    if flag:
        ID = await add_question_id(NAME)
    await add_question(str(message.text), ID) # вопросу по ID передается вопрос
    await QCreation.RightAnsw.set()
    global c
    c = 1
    flag=True
    await message.answer("Введите верный вариант ответа")

#handler(right answer)
async def enter_right_answer(message: types.Message):
    await add_right_answer(str(message.text), ID)
    await QCreation.WrongAnsw.set()
    await message.answer("Введите неверный вариант ответа")


#handler (wrong answ)
async def enter_wrong_answer(message: types.Message):
    global c, UserID 
    UserID = message.from_user.id
    if c <= 3:
        await add_wrong_answer(str(message.text), c, ID)
        if c == 3:
            await message.answer("Вы ввели максимальное количетво ответов",reply_markup=DoneQuestButt)
        else:
            await message.answer('Нажмите "готово", если вы завершили создание вопроса, нажмите "добавить", чтобы добавить'
                                ' дополнительный неверный вариант ответа',reply_markup=InlnQuestionButtons)
        c+=1
    else:
        await message.answer("Вы ввели максимальное количетво ответов",reply_markup=DoneQuestButt)


async def question_is_done(callback: types.CallbackQuery):
    await QCreation.question.set()
    await callback.message.answer("Введите вопрос или нажмите готово для завершения создания викторины",
                                  reply_markup=DoneQuizButt)


async def next_wrong_answer(callback: types.CallbackQuery):
    await QCreation.WrongAnsw.set()
    await callback.message.answer("Введите неверный вариант ответа")


async def quiz_is_done(callback: types.CallbackQuery, state: FSMContext):
    global UserID
    await callback.message.answer("Викторина создана!", reply_markup=Start_Markup)
    await state.finish()
    await Enter_User_QuizCreated(UserID)


def reg_QuizCreation_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(add_quiz, text="NewQuiz", state="*")
    dp.register_message_handler(enter_quiz_name, state=QCreation.name)
    dp.register_message_handler(enter_question, state=QCreation.question)
    dp.register_message_handler(enter_right_answer, state=QCreation.RightAnsw)
    dp.register_message_handler(enter_wrong_answer, state=QCreation.WrongAnsw)
    dp.register_callback_query_handler(question_is_done, text="QuestDone", state="*")
    dp.register_callback_query_handler(next_wrong_answer, text="NextAnsw", state="*")
    dp.register_callback_query_handler(quiz_is_done, text="QuizDone", state="*")
