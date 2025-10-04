from flask import Blueprint, url_for, request, redirect, render_template, abort
import datetime
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'

@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {"name": "роза", "price": 100},
    {"name": "тюльпан", "price": 70},
    {"name": "незабудка", "price": 50},
    {"name": "ромашка", "price": 40},
]

@lab2.route('/lab2/flowers/', methods=['GET', 'POST'])
def all_flowers():
    if request.method == 'POST':
        name = request.form.get("name")
        price = request.form.get("price")
        if not name or not price:
            return "Ошибка: не заданы имя или цена", 400
        flower_list.lab2end({"name": name, "price": int(price)})
        return redirect("/lab2/flowers/")
    
    return render_template("flowers.html", flowers=flower_list)

@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    return "вы не задали имя цветка", 400

@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers/')

@lab2.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers/')

@lab2.route('/lab2/example')
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

@lab2.route('/lab2/')
def labd(): 
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)



@lab2.route('/lab2/calc/<int:a>/<int:b>')
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

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
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

@lab2.route('/lab2/books')
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

@lab2.route('/lab2/cars')
def cars_gallery():
    return render_template('cars.html', cars=cars)

@lab2.route('/')
def indexd():
    return render_template('base.html') 