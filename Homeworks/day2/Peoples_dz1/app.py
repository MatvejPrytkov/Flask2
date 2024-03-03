# С помощью библиотеки faker создать 3 файла:
# 1. humans.txt - ФИО(hint -> .name()), разделитель - запятая
# 2. names.txt - Имена(hint -> .first_name())
# 3. users.txt - Профиль(hint -> .simple_profile()), разделитель - запятая

# Создать по 10 строк в каждом файле
from flask import Flask, render_template, abort, g
from faker import Faker
import sqlite3


app = Flask(__name__)
fake = Faker("ru_RU")

#print(app.default_config)
app.config.from_object("config.Config")
#print(app.config)

def create_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, login VARCHAR(15),
                      first_name VARCHAR(15), middle_name VARCHAR(15), last_name VARCHAR(15), 
                      sex VARCHAR(1), address VARCHAR(50), mail VARCHAR(15), birthdate DATE)''')
    conn.close()


def create_table():
    for _ in range(10):
        #Открываем соединение с базой данных 
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()

        fake_user = fake.simple_profile()
        login = fake_user.get("username") 
        name  = fake_user.get("name")
        name = name.split(' ')
        first_name = name[0]
        middle_name = name[1]
        last_name = name[2]
        sex   = fake_user.get("sex")
        address = fake_user.get("address")
        mail = fake_user.get("mail")
        birthdate = fake_user.get("birthdate")
        #.strftime("%d/%m/%Y %H:%M:%S")
        #print(login, first_name, middle_name, last_name, sex, address, mail, birthdate)

        # добавляем новую запись в таблицу users
        cursor.execute("""
                       INSERT INTO users (login, first_name, middle_name, last_name, sex, address, mail, birthdate) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                       (login, first_name, middle_name, last_name, sex, address, mail, birthdate)
                       )

        # Сохраняем изменения и закрываем соединение с базой
        conn.commit()
        conn.close()


def print_db():
    #создаем соединение нашей базой данных
    conn = sqlite3.connect(app.config['DATABASE'])
    #создаем курсор
    cursor = conn.cursor()
    with conn:
        #cursor.execute("SELECT * FROM users")
        #print(cursor.fetchall())
        #выполняем запрос к таблицe
        cursor.execute("""SELECT login, first_name, middle_name, last_name, sex, address, mail, birthdate FROM users""")
        #получаем результат запроса
        #result = cursor.fetchone()
        rows = cursor.fetchall()
        for row in rows:
            #print(row)
            login, first_name, middle_name, last_name, sex, address, mail, birthdate = row
            print(login, first_name, middle_name, last_name, sex, address, mail, birthdate)
    #закрываем соединение с базой данных
    conn.close()


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn


def get_db():
    #переменная g контекста приложения
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db    


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()
    

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/names")
def get_names():
    names = list()
    db = get_db()
    cursor = db.cursor()
    with db:
        cursor.execute("""SELECT first_name FROM users""")
        rows = cursor.fetchall()
        for row in rows:
            first_name, = row
            names.append(first_name)
    return render_template("names.html", people_names=names)


@app.route("/table")
def table():
    peoples = list()
    db = get_db()
    cursor = db.cursor()
    with db:
        cursor.execute("""SELECT first_name, middle_name, last_name FROM users""")
        rows = cursor.fetchall()
        for row in rows:
            first_name, middle_name, last_name = row
            peoples.append({
                'last_name': last_name,
                'middle_name': middle_name, 
                'first_name': first_name})
    return render_template('table.html', peoples=peoples)


@app.route("/users")
def users_list():
    peoples = list()
    db = get_db()
    cursor = db.cursor()
    with db:
        cursor.execute("""SELECT login, first_name, middle_name, last_name, sex, birthdate, mail FROM users""")
        rows = cursor.fetchall()
        for row in rows:
            login, first_name, middle_name, last_name, sex, birthdate, mail = row
            peoples.append({
                'login': login,
                'sex': sex, 
                'fio': first_name+' '+middle_name+' '+last_name,
                'birthdate':birthdate,
                'mail':mail})
    return render_template('users_list.html', peoples=peoples)


@app.route("/users/<login>")
def user_item(login):

    item = None
    db = get_db()
    cursor = db.cursor()
    with db:
        cursor.execute("SELECT login, first_name, middle_name, last_name, sex, birthdate, mail FROM users WHERE login=\'"+login+"\'")
        row = cursor.fetchone()

        if row:
            login, first_name, middle_name, last_name, sex, birthdate, mail = row
            item = {'login': login, 'sex': sex, 'fio': first_name+' '+middle_name+' '+last_name,
                'birthdate':birthdate, 'mail':mail}
            return render_template('user_item.html', item=item)

    return abort(404)


if __name__ == "__main__":
    #create_db()
    #create_table()
    #print_db()
    app.run(debug=True)

