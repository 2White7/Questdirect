import sqlite3
from datetime import datetime, timedelta

mainid = 0

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
        date TEXT,
        duration INTEGER,
        location TEXT,
        traveltime INTEGER,
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
    mon = int(input("Введите месяц в котором планируется задача (в цифрах): "))
    d = int(input("Введите день на который запланирована задача: "))
    h = int(input("Введите час на который запланирована задача: "))
    m = int(input("Введите минуты для указания точного времени: "))
    date = datetime(y, mon, d, h, m)
    h1 = int(input("Введите сколько часов вы планируете на задачу: "))
    if h1 >= 24:
        print("К сожалению в сутках 24 часа")
        return
    m1 = int(input("Введите сколько минут вы планируете на задачу: "))
    if m1 >= 60:
        print("Так нельзя, в одном часу 60 минут")
        return
    duration = timedelta(hours=h1, minutes=m1)
    l = str(input("Введите где будет выполняться задача: "))
    h2 = int(input("Введите сколько часов вы планируете на дорогу: "))
    if h2 >= 24:
        print("К сожалению в сутках 24 часа")
        return
    m2 = int(input("Введите сколько минут вы планируете на дорогу: "))
    if m2 >= 60:
        print("Так нельзя, в одном часу 60 минут")
        return
    travel_time = timedelta(hours=h2, minutes=m2)
    st = "Не выполнено"

    start_time = date - travel_time
    end_time = date + duration

    try:
        db = sqlite3.connect("qdiary.db")
        cursor = db.cursor()

        # проверка наложения задач друг на друга
        overlapping_tasks = cursor.execute("""
            SELECT * FROM tasks WHERE
            (
                (date BETWEEN ? AND ?) OR
                (date + duration BETWEEN ? AND ?) OR
                (? BETWEEN date AND date + duration) OR
                (? BETWEEN date - traveltime AND date + duration + traveltime)
            )
            AND mainid = ? AND status = ?""",
                                           (start_time, end_time, start_time, end_time, start_time, end_time, mainid,
                                            st)).fetchone()

        if overlapping_tasks:
            print("Время задачи пересекается с другой задачей")
            return

        # проверка возможности выполнения задачи в течение текущего дня
        if start_time.date() != end_time.date() or end_time > datetime.max or start_time < datetime.now():
            print('Новая задача не помещается в текущий день. Перенесите на следующий день')
            return

        duration_hours = duration.total_seconds() / 3600
        travel_hours = travel_time.total_seconds() / 3600
        date = str(date)
        values = [mainid, ntask, dtask, date, duration_hours, travel_hours, l, st]
        cursor.execute("""INSERT INTO tasks(mainid, ntask, dtask, date,
            duration, traveltime, location, status) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", values)
        db.commit()
        print("Задача создана успешно")
    except sqlite3.Error as e:
        print("Ошибка при выполнении операции в базе данных:", e)
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
        d2 = int(input("Введите статус задачи (1-выполнено, 2-не выполнено, 3-вернутся): "))

        if d2 == 1:
            id = d1
            cursor.execute("UPDATE tasks SET status = 'Выполнено' WHERE asistid = ?", [id])
            db.commit()
        elif d2 == 2:
            id = d1
            cursor.execute("UPDATE tasks SET status = 'Не выполнено' WHERE asistid = ?", [id])
            db.commit()
        elif d2 == 3:
            inteface()
        else:
            print("Выберете 1, 2 или 3")
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
main()
