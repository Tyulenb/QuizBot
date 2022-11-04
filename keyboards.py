from subprocess import call
from config import InlineKeyboardMarkup, InlineKeyboardButton
# inline кнопки


InlnQuestionButtons = InlineKeyboardMarkup(row_width=1) # сбор butt 1 и butt 2
DoneQuestButt = InlineKeyboardMarkup(row_width=1) # Butt1
DoneQuizButt = InlineKeyboardMarkup(row_width=1) # Butt3
Butt1=InlineKeyboardButton(text="Готово", callback_data="QuestDone")  # завершение создания вопроса
Butt2=InlineKeyboardButton(text="Добавить", callback_data="NextAnsw") # добавить новый неверный ответ
Butt3=InlineKeyboardButton(text="Готово", callback_data="QuizDone") # завершить создание викторины
InlnQuestionButtons.add(Butt1,Butt2)
DoneQuestButt.add(Butt1)
DoneQuizButt.add(Butt3)


Start_Markup = InlineKeyboardMarkup(row_width=1) # кнопка вызова меню
SolveQuiz_NewQuiz_Markup = InlineKeyboardMarkup(row_width=1)
QuizList_Markup = InlineKeyboardMarkup(row_width=1)
SolveQuiz = InlineKeyboardButton(text="Пройти викторину", callback_data="Solve") # пройти викторину
NewQuizButt = InlineKeyboardButton(text="Создать Викторину", callback_data="NewQuiz") # создать викторину
ListButt = InlineKeyboardButton(text="Список Викторин", callback_data="list") # получить список викторин
Cancel_Button = InlineKeyboardButton(text="Отменить прохождение", callback_data="Cancel") # отменить прохождение викторины
QuizList_Markup.add(ListButt,Cancel_Button)
SolveQuiz_NewQuiz_Markup.add(NewQuizButt,SolveQuiz)
Start_Markup.add(NewQuizButt,ListButt,SolveQuiz)


Show_correct_Answ_Markup = InlineKeyboardMarkup(row_width=1)
Show_correct_Answ = InlineKeyboardButton(text="Показать ответы", callback_data="Show_Correct_Answers")
Show_correct_Answ_Markup.add(Show_correct_Answ, ListButt)