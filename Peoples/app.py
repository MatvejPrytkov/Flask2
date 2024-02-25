# С помощью библиотеки faker создать 3 файла:
# 1. humans.txt - ФИО(hint -> .name()), разделитель - запятая
# 2. names.txt - Имена(hint -> .first_name())
# 3. users.txt - Профиль(hint -> .simple_profile()), разделитель - запятая

# Создать по 10 строк в каждом файле
from flask import Flask, render_template
from faker import Faker


app = Flask(__name__)
fake = Faker("ru_RU")


def create_files() -> None:
    """ Function to create txt files."""
    with open("./files/humans.txt", 'w', encoding="utf-8") as humans_f:
        for _ in range(10):
            print(*fake.name().split(), sep=',', file=humans_f)

    with open("./files/names.txt", 'w', encoding="utf-8") as humans_f:
        for _ in range(10):
            print(fake.first_name(), sep=',', file=humans_f)

    with open("./files/users.txt", 'w', encoding="utf8") as humans_f:
        for _ in range(10):
            print(*fake.simple_profile().values(), sep=';', file=humans_f)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/names")
def get_names():
    names = list()
    with open("./files/names.txt", encoding="utf-8") as f:
        for raw_line in f:
            names.append(raw_line.strip())
    return "<br>".join(names)


if __name__ == "__main__":
    # create_files()
    app.run(debug=True)