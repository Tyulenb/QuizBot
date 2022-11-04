import sqlite3 as sq
from config import types

base = sq.connect("based.db")
cur = base.cursor()

#методы для создания викторины

async def add_quiz_name(arg):
    cur.execute("INSERT INTO quiz(name) VALUES(?)", (arg,))
    base.commit()


async def add_question_id(NAME):
    ID = cur.execute("SELECT rowid FROM quiz WHERE name == ?", (NAME,)).fetchall()[-1][0]
    cur.execute("INSERT INTO questions(ID) VALUES(?)", (ID,))
    IDquest = cur.execute("SELECT rowid FROM questions WHERE ID == ?", (ID,)).fetchall()[-1][0]
    base.commit()
    return IDquest

async def add_question(arg, ID):
    cur.execute("UPDATE questions SET quest = ? WHERE rowid == ?", (arg,ID,))
    base.commit()


async def add_right_answer(arg, ID):
    cur.execute("UPDATE questions SET Ransw = ? WHERE rowid == ?", (arg,ID,))
    base.commit()


async def add_wrong_answer(arg, c, ID):
    cur.execute(f"UPDATE questions SET WAnsw{c} = ? WHERE rowid == ?", (arg,ID,))
    base.commit()

#методы для прохождения викторины

async def Quiz_list():
    string = ""
    arr = cur.execute("SELECT rowid FROM quiz").fetchall()
    for elem in range(0,len(arr)):
        i = cur.execute("SELECT name FROM quiz WHERE rowid == ?", (arr[elem][0],)).fetchall()[0][0] # название викторины с id из списка
        string += "Название: " + str(i) + " " + "id : " + str(arr[elem][0]) + "\n"
    return string


async def Get_quest(ID):
    i=cur.execute("SELECT quest, Ransw, WAnsw1, WAnsw2, WAnsw3 FROM questions WHERE ID == ?",(ID,)).fetchall()
    return i


async def Get_Quiz_Name(ID):
    Name = cur.execute("SELECT name FROM quiz WHERE rowid == ?", (ID,)).fetchall()[0][0]
    return Name


#методы для работы с пользователями

async def Enter_User_Id(id):
    existence_checker = cur.execute("SELECT rowid FROM users WHERE UserID==?",(id,)).fetchone()
    if existence_checker is None:
        cur.execute("INSERT INTO users(UserID) VALUES(?)", (id,))
        base.commit()
    else:
        return


async def Enter_User_AmountOfAnsw(id, NewAnsw):
    current_amount = cur.execute("SELECT AmountOfAnsw FROM users WHERE UserID == ?",(id,)).fetchone()[0]
    if current_amount == None:
        current_amount=0
    cur.execute("UPDATE users SET AmountOfAnsw = ? WHERE UserId == ?", (int(current_amount)+int(NewAnsw),id,))
    base.commit()


async def Enter_User_Ransw(id, NewRightAnsw):
    current_amount = cur.execute("SELECT RAnsw FROM users WHERE UserID == ?",(id,)).fetchone()[0]
    if current_amount == None:
        current_amount=0
    cur.execute("UPDATE users SET RAnsw = ? WHERE UserId == ?", (int(current_amount)+int(NewRightAnsw),id,))
    base.commit()


async def Enter_User_QuizCompleted(id):
    current_amount = cur.execute("SELECT QuizCompleted FROM users WHERE UserID == ?",(id,)).fetchone()[0]
    if current_amount == None:
        current_amount=0
    cur.execute("UPDATE users SET QuizCompleted = ? WHERE UserId == ?", (int(current_amount)+1,id,))
    base.commit()


async def Enter_User_QuizCreated(id):
    current_amount = cur.execute("SELECT QuizCreated FROM users WHERE UserID == ?",(id,)).fetchone()[0]
    if current_amount == None:
        current_amount=0
    cur.execute("UPDATE users SET QuizCreated = ? WHERE UserId == ?", (int(current_amount)+1,id,))
    base.commit()


async def Get_User_Percentage(id):
    Ransw = cur.execute("SELECT RAnsw FROM users WHERE UserID == ?",(id,)).fetchone()[0]
    AmountOfAnsw = cur.execute("SELECT AmountOfAnsw FROM users WHERE UserID == ?",(id,)).fetchone()[0]
    if(AmountOfAnsw==None):
        return "-"
    result = str(int(Ransw)/int(AmountOfAnsw)*100)+"%"
    return result


async def Get_User_Stats(id):
    stats = cur.execute("SELECT QuizCompleted, AmountOfAnsw, RAnsw, QuizCreated FROM users WHERE UserId == ?",(id,)).fetchone()
    return stats
