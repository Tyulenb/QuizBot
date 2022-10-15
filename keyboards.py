from config import InlineKeyboardMarkup, InlineKeyboardButton
# inline кнопки
InlnQuestionButtons = InlineKeyboardMarkup(row_width=1) # сбор butt 1 и butt 2
DoneQuestButt = InlineKeyboardMarkup(row_width=1) # Butt1
DoneQuizButt = InlineKeyboardMarkup(row_width=1) # Butt3

Butt1=InlineKeyboardButton(text="Готово", callback_data="QuestDone")  # завершение создания вопроса
Butt2=InlineKeyboardButton(text="Добавить", callback_data="NextAnsw") # добавить новый неверный ответ
Butt3=InlineKeyboardButton(text="Готово", callback_data="QuizDone") # завершить создание викторины

NewQuizButt=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Создать Викторину", callback_data="NewQuiz"))

InlnQuestionButtons.add(Butt1,Butt2)
DoneQuestButt.add(Butt1)
DoneQuizButt.add(Butt3)