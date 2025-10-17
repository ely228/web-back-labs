from flask import Blueprint, render_template, request, make_response, redirect, url_for

lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'unknown'
    name_color = request.cookies.get('name_color') or '#000000'
    age = request.cookies.get('age') or 'не указан'

    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)



@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    
    sex = request.args.get('sex')
    
    return render_template('lab3/form1.html', 
                         user=user, 
                         age=age, 
                         sex=sex, 
                         errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    text_color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    if text_color or bg_color or font_size or font_style:
        resp = make_response(redirect('/lab3/settings'))
        if text_color:
            resp.set_cookie('color', text_color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp

    return render_template('lab3/settings.html',
        color=request.cookies.get('color'),
        bg_color=request.cookies.get('bg_color'),
        font_size=request.cookies.get('font_size'),
        font_style=request.cookies.get('font_style')
    )

@lab3.route('/lab3/train')
def train():
    errors = {}
    fio = request.args.get('fio', '').strip()
    shelf = request.args.get('shelf', '')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age', '')
    departure = request.args.get('departure', '').strip()
    destination = request.args.get('destination', '').strip()
    date = request.args.get('date', '')
    insurance = request.args.get('insurance')

    if request.args:
        if not fio:
            errors['fio'] = 'Введите ФИО'
        if not shelf:
            errors['shelf'] = 'Выберите полку'
        if not age or not age.isdigit() or not (1 <= int(age) <= 120):
            errors['age'] = 'Укажите корректный возраст'
        if not departure:
            errors['departure'] = 'Укажите пункт выезда'
        if not destination:
            errors['destination'] = 'Укажите пункт назначения'
        if not date:
            errors['date'] = 'Укажите дату'

        if not errors:
            price = 1000 if int(age) >= 18 else 700
            if shelf in ['нижняя', 'нижняя боковая']:
                price += 100
            if linen:
                price += 75
            if baggage:
                price += 250
            if insurance:
                price += 150
            ticket_type = 'Детский билет' if int(age) < 18 else 'Взрослый билет'
            return render_template('lab3/train_ticket.html',
                                   fio=fio,
                                   shelf=shelf,
                                   linen=bool(linen),
                                   baggage=bool(baggage),
                                   age=age,
                                   departure=departure,
                                   destination=destination,
                                   date=date,
                                   insurance=bool(insurance),
                                   price=price,
                                   ticket_type=ticket_type)

    return render_template('lab3/train_form.html',
                           errors=errors,
                           fio=fio,
                           shelf=shelf,
                           linen=linen,
                           baggage=baggage,
                           age=age,
                           departure=departure,
                           destination=destination,
                           date=date,
                           insurance=insurance)

@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_style')
    return resp


products = [
    {"name": "BMW M3 G80", "price": 7890000, "weight": "1730 кг", "color": "синий"},
    {"name": "BMW M5 F90", "price": 9890000, "weight": "1855 кг", "color": "черный"},
    {"name": "BMW i4 M50", "price": 8690000, "weight": "2125 кг", "color": "белый"},
    {"name": "Audi A6", "price": 5690000, "weight": "1650 кг", "color": "серебристый"},
    {"name": "Audi S6", "price": 7490000, "weight": "1800 кг", "color": "черный"},
    {"name": "Audi Q5", "price": 5290000, "weight": "1800 кг", "color": "белый"},
    {"name": "Audi Q8", "price": 7990000, "weight": "2150 кг", "color": "серый"},
    {"name": "Porsche Macan GTS", "price": 9490000, "weight": "1960 кг", "color": "зеленый"},
    {"name": "Porsche Cayenne Turbo", "price": 12990000, "weight": "2250 кг", "color": "черный"},
    {"name": "Porsche 911 Carrera", "price": 14990000, "weight": "1500 кг", "color": "желтый"},
    {"name": "Lexus RX 350", "price": 6290000, "weight": "2000 кг", "color": "серебристый"},
    {"name": "Lexus LX 600", "price": 12900000, "weight": "2600 кг", "color": "белый"},
    {"name": "Toyota Land Cruiser 300", "price": 8990000, "weight": "2580 кг", "color": "черный"},
    {"name": "Kia K5 GT", "price": 3490000, "weight": "1570 кг", "color": "синий"},
    {"name": "Hyundai Tucson", "price": 2990000, "weight": "1580 кг", "color": "серый"},
    {"name": "Mercedes-Benz C200", "price": 4990000, "weight": "1655 кг", "color": "синий"},
    {"name": "Mercedes-Benz E300", "price": 6590000, "weight": "1780 кг", "color": "черный"},
    {"name": "Mercedes-Benz GLE 450", "price": 9490000, "weight": "2185 кг", "color": "белый"},
    {"name": "Mercedes-Benz GLS 600 Maybach", "price": 18500000, "weight": "2700 кг", "color": "золотой"},
    {"name": "Mercedes-Benz AMG GT 63 S", "price": 16990000, "weight": "2045 кг", "color": "красный"},
    {"name": "BMW X5 M Competition", "price": 11990000, "weight": "2300 кг", "color": "серый"},
    {"name": "BMW X6 M50i", "price": 10790000, "weight": "2250 кг", "color": "красный"},
    {"name": "Audi RS6 Avant", "price": 10990000, "weight": "2075 кг", "color": "красный"},
]


@lab3.route('/lab3/products')
def products_page():
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    min_price = min(p["price"] for p in products)
    max_price = max(p["price"] for p in products)

    user_min = request.args.get('min_price', type=int) or (int(min_price_cookie) if min_price_cookie else min_price)
    user_max = request.args.get('max_price', type=int) or (int(max_price_cookie) if max_price_cookie else max_price)

    if user_min > user_max:
        user_min, user_max = user_max, user_min

    filtered = [p for p in products if user_min <= p["price"] <= user_max]

    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered,
        count=len(filtered),
        min_price=user_min,
        max_price=user_max,
        min_price_all=min_price,
        max_price_all=max_price
    ))

    resp.set_cookie('min_price', str(user_min))
    resp.set_cookie('max_price', str(user_max))

    return resp

@lab3.route('/lab3/products/reset')
def reset_products():
    resp = make_response(redirect('/lab3/products'))
    resp.delete_cookie('min_price')
    resp.delete_cookie('max_price')