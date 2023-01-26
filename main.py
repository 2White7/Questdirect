import sqlite3
import datetime

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
        long TEXT,
        location TEXT,
        time TEXT,
        status INTEGER
    )
    """

    cursor.executescript(query)

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

def createtask():
    ntask = str(input("Введите название задачи: "))
    dtask = str(input("Введите описание задачи: "))
    y = int(input("Введите год в котором планируется задача: "))
    mon = int(input("Введите месяц в котором планируется задача(в цифрах): "))
    d = int(input("Введите день на который запланирована задача: "))
    h = int(input("Введите час на который запланирована задача: "))
    m = int(input("Введите минуты для указания точного времени: "))
    date = datetime.datetime(y, mon, d, h, m)
    h1 = int(input("Сколько часов вы планируете на задачу: "))
    #if h1 > 25:
        #print("")
    m1 = int(input("Сколько минут вы планируете на задачу: "))
    long = datetime.time(h1, m1)
    print(long)
def inteface():
    a = int(input())
    if a == 1:
        registration()
    elif a == 2:
        pass
    elif a == 3:
        pass
    elif a == 4:
        pass
    elif a == 5:
        pass
    elif a == 6:
        pass
    elif a == 7:
        return a
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
createtask()