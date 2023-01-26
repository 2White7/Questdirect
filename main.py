import sqlite3
import datetime

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
        long TEXT,
        location TEXT,
        time TEXT,
        status INTEGER
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
    pass

# функция создания задачи
def createtask():
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
    long = datetime.time(h1, m1)
    l = str(input("Введите где будет выполнятся задача: "))
    h2 = int(input("Введите сколько часов планируется на дорогу: "))
    m2 = int(input("Введите сколько минут планируется на дорогу"))
    tt = datetime.time(h2, m2)
    #st = 0 блок проверки на статус выполнения задачи быть ему не тут
    #if st == 0:
        #st1 = "Не выполнено"
    #else:
        #st1 = "Выполнено"

# функция выполнено/не выполнено
def markdone():
    d1 = int(input("Введите айди задачи: "))
    d2 = int(input("Введите статус задачи (1-выполнено, 2-не выполнено): "))

# вывод выполненых задач
def done():
    pass

# вывод не выполненых задач
def notdone():
    pass

# функция интерфейса
def inteface():
    a = int(input())
    if a == 1:
        registration()
    elif a == 2:
        account()
    elif a == 3:
        createtask()
    elif a == 4:
        markdone()
    elif a == 5:
        done()
    elif a == 6:
        notdone()
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
