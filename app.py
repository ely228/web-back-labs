from flask import Flask, url_for, request, redirect, abort, render_template, session
import datetime
from flask_sqlalchemy import SQLAlchemy
from lab8_db import db
from os import path

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from rgz import rgz
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретный_ключ123')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
  db_name = 'ilya_zubricki_orm'
  db_user = 'ilya_zubricki_orm'
  db_password = '123'
  host_ip = '127.0.0.1'
  host_port = 5432
  app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
  dir_path = path.dirname(path.realpath(__file__))
  db_path = path.join(dir_path, "ilya_zubricki_orm.db")
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://{db_path}'

db.init_app(app)
print("DATABASE URI:", app.config['SQLALCHEMY_DATABASE_URI'])

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(rgz)


@app.errorhandler(404)
def not_found(err):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr
    url = request.url

    entry = f"{time} — {ip} — {url}"
    journal.append(entry)

    log_html = "<h3>Журнал:</h3><ul>"
    for record in journal[-10:]:
        log_html += f"<li>{record}</li>"
    log_html += "</ul>"
    img = url_for('static', filename='404.png')
    return f'''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Ошибка 404</title>
    <style>
      body {{
        background: white;
        color: black;
        font-family: Arial;
        text-align: center;
        padding: 40px;
      }}
      h1 {{
        color: black;
      }}
      img {{
        width: 250px;
        margin: 20px;
      }}
      .journal {{
        text-align: left;
        margin-top: 30px;
      }}
    </style>
</head>
<body>
  <h1>Страница не найдена</h1>
  <p><b>Ваш IP:</b> {ip}</p>
  <p><b>Дата и время:</b> {time}</p>
  <p><a href="/">Вернуться на главную</a></p>
  <img src="{img}" alt="404">
  <div class="journal">
    {log_html}
  </div>
</body>
</html>''', 404

journal = []

@app.route('/')
@app.route('/index')
def index():
    return '''<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='lab1/main.css') }}">
        <link rel="icon" type="image/png" href="{{ url_for('static', filename='lab2/favicon.ico', v=2) }}">
    </head>
    <body>
        <header>
            WEB-программирование, часть 2. Главная страница
            <nav>
                <a href="/">Главное меню</a>
            </nav>
        </header>
        <main>
            <h1>НГТУ, ФБ, Лабораторные работы</h1>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                    <li><a href="/lab3">Третья лабораторная</a></li>
                    <li><a href="/lab4">Четвертая лабораторная</a></li>
                    <li><a href="/lab5/">Пятая лабораторная</a></li>
                    <li><a href="/lab6">Шестая лабораторная</a></li>
                    <li><a href="/lab7">Седьмая лабораторная</a></li>
                    <li><a href="/lab8">Восьмая лабораторная</a></li>
                    <li><a href="/rgz/">РГЗ</a></li>
                </ul>
            </nav>
        </main>
        <footer>
            &copy; Зубрицкий Илья, ФБИ-34, 3 курс, 2025
        </footer>
    </body>
</html>'''


@app.errorhandler(500)
def handle_500(err):
    return '''<!doctype html>
<html>
<head><meta charset="utf-8"><title>Ошибка 500</title></head>
<body>
  <h1>Внутренняя ошибка сервера (500)</h1>
  <p>Произошла ошибка. Попробуйте позже.</p>
  <a href="/">На главную</a>
</body>
</html>''', 500




