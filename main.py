import sqlite3
import datetime

mainid = 8

#блок создания таблиц
with sqlite3.connect("qdiary.db") as db:
    cursor = db.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name VARCHAR(15),
        login VARCHAR(30)
    );
    CREATE TABLE IF NOT EXISTS tasks(
        mainid INTEGER,
        asistid INTEGER PRIMARY KEY,
        ntask VARCHAR(40),
        dtask TEXT,
        date DATETIME,
        long TIME,
        location TEXT,
        time TIME,
        status VARCHAR(15)
    )
    """

    cursor.executescript(query)

#функция регистрации пользователя, по задумке можно будет на разных акках чекать разные задачи
def registration():
    name = input("Введите имя: ")
    login = input("Введите логин: ")
    try:
        db = sqlite3.connect("qdiary.db")
        cursor = db.cursor()

        cursor.execute("SELECT login FROM users WHERE login = ?", [login])
        if cursor.fetchone() is None:
            values = [name, login]
            cursor.execute("INSERT INTO users(name, login) VALUES (?, ?)", values)
            db.commit()
            print("Регистрация успешна")
        else:
            print("Логин уже занят")
            registration()
    except sqlite3.Error as e:
        print("Erorr", e)
    finally:
        cursor.close()
        db.close()

# вход в акк
def account():
    global mainid
    login = input("Введите логин: ")
    cursor.execute("SELECT login FROM users WHERE login = ?", [login])
    if cursor.fetchone() is None:
        print("Такого логина не существует")
    else:
        [mainid], = cursor.execute("SELECT id FROM users WHERE login = ?", [login])
        print("Вход выполнен")

# функция создания задачи
def createtask():
    global mainid
    ntask = str(input("Введите название задачи: "))
    dtask = str(input("Введите описание задачи: "))
    y = int(input("Введите год в котором планируется задача: "))
    mon = int(input("Введите месяц в котором планируется задача(в цифрах): "))
    d = int(input("Введите день на который запланирована задача: "))
    h = int(input("Введите час на который запланирована задача: "))
    m = int(input("Введите минуты для указания точного времени: "))
    date = datetime.datetime(y, mon, d, h, m)
    h1 = int(input("Введите сколько часов вы планируете на задачу: "))
    #if h1 > 25: проверка на дебила 1(если ввести больше 24 дейттайм крашит нахер)
        #print("К сожалению в сутках 24 часа")
    m1 = int(input("Введите сколько минут вы планируете на задачу: "))
    #if m1 > 60: проверка на дебила 2(суть та же что и в 1 но с минутами)
        #print("Так нельзя, в одном часу 60 минут")
    long = datetime.datetime(y, mon, d, h1, m1)
    l = str(input("Введите где будет выполнятся задача: "))
    h2 = int(input("Введите сколько часов планируется на дорогу: "))
    m2 = int(input("Введите сколько минут планируется на дорогу: "))
    tt = datetime.datetime(y, mon, d, h2, m2)
    st = "Не выполнено"
    try:
        db = sqlite3.connect("qdiary.db")
        cursor = db.cursor()
        values = [mainid, ntask, dtask, date, long, l, tt, st]
        cursor.execute("""INSERT INTO tasks(mainid, ntask, dtask, date,
        long, location, time, status) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", values)
        db.commit()
        print("Задача создана успешно")
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()

# функция выполнено/не выполнено
def markdone():
    global mainid
    try:
        db = sqlite3.connect("qdiary.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE mainid = ?", [mainid])
        print(cursor.fetchall())
        d1 = int(input("Введите айди задачи: "))
        d2 = int(input("Введите статус задачи (1-выполнено, 2-не выполнено): "))

        if d2 == 1:
            id = d1
            cursor.execute("UPDATE tasks SET status = 'Выполнено' WHERE asistid = ?", [id])
            db.commit()
        elif d2 == 2:
            id = d1
            cursor.execute("UPDATE tasks SET status = 'Не выполнено' WHERE asistid = ?", [id])
            db.commit()
        else:
            print("Выберете 1 или 2")
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()

# вывод выполненых задач
def done():
    global mainid
    try:
        db = sqlite3.connect("qdiary.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE mainid = ? AND status = ?", [mainid, 'Выполнено'])
        print(cursor.fetchall())
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()

# вывод не выполненых задач
def notdone():
    global mainid
    try:
        db = sqlite3.connect("qdiary.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE mainid = ? AND status = ?", [mainid, 'Не выполнено'])
        print(cursor.fetchall())
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()

# функция интерфейса
def inteface():
    a = int(input())
    if a == 1:
        registration()
    elif a == 2:
        account()
    elif a == 3 and mainid !=0:
        createtask()
    elif a == 4 and mainid !=0:
        markdone()
    elif a == 5 and mainid !=0:
        done()
    elif a == 6 and mainid !=0:
        notdone()
    elif a == 7:
        return a
    else:
        if a == 3 or a == 4 or a == 5 or a == 6:
            print("Войдите в аккаунт или зарегестрируйтесь")
        else:
            print("Выберите действие из списка")

def main():
    print("""Что вы хотите сделать?
                1)Создать аккаунт
                2)Войти в аккаунт
                3)Создать задачу
                4)Отметить выполнение задачи
                5)Проверить выполненые задачи
                6)Проврить не выполненые задачи
                7)Выход""")

    end = 0
    while end != 7:
        end = inteface()
    else:
        return 0

try:
    db = sqlite3.connect("qdiary.db")
    cursor = db.cursor()
    cursor.execute("SELECT date FROM tasks WHERE mainid = ?",[mainid])
    date1 = cursor.fetchone("SELECT SUBDATE")
    date2 = datetime.datetime(2023, 1, 27, 18, 0, 0)
    c = date1 - date2
    print(c)
except sqlite3.Error as e:
    print("Error", e)
finally:
    cursor.close()
    db.close()