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