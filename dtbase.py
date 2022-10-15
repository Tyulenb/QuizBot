import sqlite3 as sq
from config import types

base = sq.connect("based.db")
cur = base.cursor()

async def add_quiz_name(a):
    cur.execute("INSERT INTO quiz(name) VALUES(?)", (a,))
    base.commit()


async def add_question_id(NAME):
    ID = cur.execute("SELECT rowid FROM quiz WHERE name == ?", (NAME,)).fetchall()[-1][0]
    cur.execute("INSERT INTO questions(ID) VALUES(?)", (ID,))
    IDquest = cur.execute("SELECT rowid FROM questions WHERE ID == ?", (ID,)).fetchall()[-1][0]
    base.commit()
    return IDquest

async def add_question(a, ID):
    print(ID)
    cur.execute("UPDATE questions SET quest = ? WHERE rowid == ?", (a,ID,))
    base.commit()
    print("added")


async def add_right_answer(a, ID):
    cur.execute("UPDATE questions SET Ransw = ? WHERE rowid == ?", (a,ID,))
    base.commit()


async def add_wrong_answer(a, c, ID):
    cur.execute(f"UPDATE questions SET WAnsw{c} = ? WHERE rowid == ?", (a,ID,))
    base.commit()