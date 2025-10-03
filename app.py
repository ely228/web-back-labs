from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

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

@app.route('/')
@app.route('/index')
def index():
    return '''<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header><h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1></header>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
            </ul>
        </nav>
        <footer>
            <p>Зубрицкий Илья Сергеевич, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''

@app.route('/lab1')
def lab1():
    return '''<!doctype html>
<html>
    <head><meta charset="utf-8"><title>Лабораторная 1</title></head>
<body>
    <h1>Лабораторная 1</h1>
    <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, 
    а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
    сознательно предоставляющих лишь самые базовые возможности.</p>
    <p><a href="/">На корень сайта</a></p>
    <h2>Список роутов</h2>
    <ul>
        <li><a href="/">Главная страница</a></li>
        <li><a href="/index">Index</a></li>
        <li><a href="/lab1/web">/lab1/web</a></li>
        <li><a href="/lab1/author">/lab1/author</a></li>
        <li><a href="/lab1/image">/lab1/image</a></li>
        <li><a href="/lab1/counter">/lab1/counter</a></li>
        <li><a href="/lab1/counter/clear">/lab1/counter/clear</a></li>
        <li><a href="/lab1/info">/lab1/info</a></li>
        <li><a href="/lab1/created">/lab1/created</a></li>
        <li><a href="400">400 Bad Request</a></li>
        <li><a href="401">401 Unauthorized</a></li>
        <li><a href="402">402 Payment Required</a></li>
        <li><a href="403">403 Forbidden</a></li>
        <li><a href="404">Страница не найдена (404)</a></li>
        <li><a href="405">405 Method Not Allowed</a></li>
        <li><a href="418">418 I'm a teapot</a></li>
        <li><a href="/cause_500">Внутренняя ошибка сервера (500)</a></li>
    </ul>
</body>
</html>'''

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/plain; charset=utf-8'
            }   
 
@app.route("/lab1/author")
def author():
    name = "Зубрицкий Илья Сергеевич"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
           <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
           </body>
        </html>"""

@app.route('/lab1/image')
def image():
    css = url_for('static', filename='lab1.css')
    img = url_for('static', filename='oak.jpg')
    html = f'''<!doctype html>
<html>
   <head>
    <meta charset="utf-8">
    <title>Дуб</title>
    <link rel="stylesheet" href="{css}">
</head>
<body>
    <h1>Дуб</h1>
    <img class="lab1" src="{img}" alt="Дуб">
</body>
</html>'''
    headers = {
        'Content-Language': 'ru',
        'X-Project': 'lab1',
        'X-Author': 'Zubriczkii'
    }
    return html, 200, headers

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count +=1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    clear_url = url_for('clear_counter')
    return f'''
<!doctype html>
<html>
    <head><title>Счётчик</title></head>
        <body>
            Сколько раз вы сюда заходили: {count}
            <hr>
            Дата и время: {time} <br>
            Запрошенный адрес: {url} <br>
            Ваш IP-адрес: {client_ip} <br>
            <p><a href="{clear_url}">Очистить счётчик</a></p>
        </body>
</html>'''

@app.route('/lab1//counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect(url_for('counter'))

@app.route("/lab1/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html"
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''',201

@app.route("/400")
def bad_request():
    return '''<!doctype html>
<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Сервер не может обработать запрос из-за синтаксической ошибки.</p>
</body>
</html>''', 400


@app.route("/401")
def unauthorized():
    return '''<!doctype html>
<html>
<head>
    <title>401 Unauthorized</title>
</head>
<body>
    <h1>401 Unauthorized</h1>
    <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
</body>
</html>''', 401

@app.route("/402")
def payment_required():
    return '''<!doctype html>
<html>
<head>
    <title>402 Payment Required</title>
</head>
<body>
    <h1>402 Payment Required</h1>
    <p>Для доступа к ресурсу требуется оплата.</p>
</body>
</html>''', 402

@app.route("/403")
def forbidden():
    return '''<!doctype html>
<html>
<head>
    <title>403 Forbidden</title>
</head>
<body>
    <h1>403 Forbidden</h1>
    <p>Доступ к ресурсу запрещен.</p>
</body>
</html>''', 403

@app.route("/405")
def method_not_allowed():
    return '''<!doctype html>
<html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<body>
    <h1>405 Method Not Allowed</h1>
    <p>Метод нельзя применить для данного ресурса.</p>
</body>
</html>''', 405

@app.route("/418")
def teapot():
    return '''<!doctype html>
<html>
<head>
    <title>418 I'm a teapot</title>
</head>
<body>
    <h1>418 I'm a teapot</h1>
    <p>Я чайник и не могу заваривать кофе.</p>
</body>
</html>''', 418

@app.route('/cause_500')
def cause_500():
    raise RuntimeError("Ошибка для проверки 500")

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

journal = []

journal = []

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {"name": "роза", "price": 100},
    {"name": "тюльпан", "price": 70},
    {"name": "незабудка", "price": 50},
    {"name": "ромашка", "price": 40},
]

@app.route('/lab2/flowers/', methods=['GET', 'POST'])
def all_flowers():
    if request.method == 'POST':
        name = request.form.get("name")
        price = request.form.get("price")
        if not name or not price:
            return "Ошибка: не заданы имя или цена", 400
        flower_list.append({"name": name, "price": int(price)})
        return redirect("/lab2/flowers/")
    
    return render_template("flowers.html", flowers=flower_list)

@app.route('/lab2/add_flower/')
def add_flower_no_name():
    return "вы не задали имя цветка", 400

@app.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers/')

@app.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers/')

@app.route('/lab2/example')
def example():
    name, number, group, course = 'Зубрицкий Илья', '2', 'ФБИ-34', '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, number=number, group=group, course=course, fruits=fruits)

@app.route('/lab2/')
def lab2(): 
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
    <!doctype html>
    <html>
    <head><meta charset="utf-8"><title>Калькулятор</title></head>
    <body>
        <h1>Калькулятор</h1>
        <ul>
            <li>{a} + {b} = {a + b}</li>
            <li>{a} - {b} = {a - b}</li>
            <li>{a} * {b} = {a * b}</li>
            <li>{a} / {b if b != 0 else 1} = {a / b if b != 0 else 'Нельзя делить на 0'}</li>
            <li>{a} ** {b} = {a ** b}</li>
        </ul>
        <p><a href="/lab2/">Назад</a></p>
    </body>
    </html>
    '''

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_a(a):
    return redirect(f'/lab2/calc/{a}/1')


books = [
    {'author': 'М. Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'В. Набоков', 'title': 'Лолита', 'genre': 'Роман', 'pages': 450},
    {'author': 'Ф. Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 600},
    {'author': 'Л. Толстой', 'title': 'Война и мир', 'genre': 'Роман', 'pages': 1200},
    {'author': 'А. Пушкин', 'title': 'Евгений Онегин', 'genre': 'Поэма', 'pages': 300},
    {'author': 'И. Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 350},
    {'author': 'А. Грин', 'title': 'Алые паруса', 'genre': 'Повесть', 'pages': 200},
    {'author': 'А. Беляев', 'title': 'Человек-амфибия', 'genre': 'Фантастика', 'pages': 300},
    {'author': 'Н. Гоголь', 'title': 'Мёртвые души', 'genre': 'Роман', 'pages': 400},
    {'author': 'А. Чехов', 'title': 'Вишнёвый сад', 'genre': 'Пьеса', 'pages': 120}
]

@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)


cars = [
    {"name": "BMW X5M", "desc": "BMW X5M", "img": "x5m.jpg"},
    {"name": "BMW M5 F90", "desc": "BMW M5 F90", "img": "f90.jpg"},
    {"name": "Hyundai Solaris", "desc": "Hyundai Solaris", "img": "solaris.jpg"},
    {"name": "Kia Rio", "desc": "Kia Rio", "img": "kia_rio.jpg"},
    {"name": "Volkswagen Polo", "desc": "Volkswagen Polo", "img": "polo.jpg"},
    {"name": "Ford Focus", "desc": "Ford Focus", "img": "ford_focus.jpg"},
    {"name": "Skoda Octavia", "desc": "Skoda Octavia", "img": "octavia.jpg"},
    {"name": "BMW M4 F82", "desc": "BMW M4 F82", "img": "f82.jpg"},
    {"name": "Haval Jolion", "desc": "Haval Jolion", "img": "haval_jolion.jpg"},
    {"name": "Chery Tiggo 7 Pro", "desc": "Chery Tiggo 7 Pro", "img": "chery_tiggo7.jpg"},
    {"name": "Geely Monjaro", "desc": "Geely Monjaro", "img": "geely_monjaro.jpg"},
    {"name": "Changan Uni-S", "desc": "Changan Uni-S", "img": "changan.jpg"},
    {"name": "Hyundai Creta", "desc": "Hyundai Creta", "img": "creta.jpg"},
    {"name": "RR Wraith", "desc": "Rolls-Royce Wraith", "img": "wraith.jpg"},
    {"name": "Toyota Camry", "desc": "Toyota Camry", "img": "camry.jpg"},
    {"name": "Mercedes G63 AMG", "desc": "Mercedes G63 AMG", "img": "g63.jpg"},
    {"name": "RR Cullinan", "desc": "Rolls-Royce Cullinan", "img": "cullinan.jpg"},
    {"name": "Bentley Continental GT", "desc": "Bentley Continental GT", "img": "continental_gt.jpg"},
    {"name": "Range Rover SVA", "desc": "Range Rover SVA Autobiography", "img": "sva.jpg"},
    {"name": "Audi Q7", "desc": "Audi Q7", "img": "q7.jpg"},
]

@app.route('/lab2/cars')
def cars_gallery():
    return render_template('cars.html', cars=cars)


@app.route('/')
def indexd():
    return render_template('base.html')