from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='ilya_zubriczki_knowledge_base',
            user='ilya_zubriczki_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/registe', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')

    if not login or not name or not password:
        return render_template('lab5/register.html', error='Заполните все поля', login=login, name=name)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, name) VALUES (%s, %s, %s);",
                    (login, password_hash, name))
    else:
        cur.execute("INSERT INTO users (login, password, name) VALUES (?, ?, ?);",
                    (login, password_hash, name))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/logi', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, password FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login, password FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if current_app.config['DB_TYPE'] == 'postgres':
        is_favorite = request.form.get('is_favorite') is not None
        is_public = request.form.get('is_public') is not None
    else:
        is_favorite = 1 if request.form.get('is_favorite') else 0
        is_public = 1 if request.form.get('is_public') else 0

    if not title or not article_text:
        return render_template('lab5/create_article.html',
                               error='Заполните и заголовок, и текст статьи',
                               title=title,
                               article_text=article_text)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) "
            "VALUES (%s, %s, %s, %s, %s);",
            (user_id, title, article_text, is_favorite, is_public)
        )
    else:
        cur.execute(
            "INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) "
            "VALUES (?, ?, ?, ?, ?);",
            (user_id, title, article_text, is_favorite, is_public)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT * FROM articles WHERE user_id=%s "
            "ORDER BY is_favorite DESC, id DESC;",
            (user_id,))
    else:
        cur.execute(
            "SELECT * FROM articles WHERE user_id=? "
            "ORDER BY is_favorite DESC, id DESC;",
            (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена", 404

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if current_app.config['DB_TYPE'] == 'postgres':
        is_favorite = request.form.get('is_favorite') is not None
        is_public = request.form.get('is_public') is not None
    else:
        is_favorite = 1 if request.form.get('is_favorite') else 0
        is_public = 1 if request.form.get('is_public') else 0
    
    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error="Введите данные")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles SET title=%s, article_text=%s, is_favorite=%s, is_public=%s "
            "WHERE id=%s AND user_id=%s;",
            (title, article_text, is_favorite, is_public, article_id, user_id))
    else:
        cur.execute(
            "UPDATE articles SET title=?, article_text=?, is_favorite=?, is_public=? "
            "WHERE id=? AND user_id=?;",
            (title, article_text, is_favorite, is_public, article_id, user_id))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, name FROM users ORDER BY login;")

    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, login, name, password FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id, login, name, password FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    error = None

    if request.method == 'POST':
        new_name = request.form.get('name', '').strip()
        new_password = request.form.get('password', '')
        confirm = request.form.get('password_confirm', '')

        if not new_name:
            error = 'Имя не может быть пустым'
        elif new_password:
            if new_password != confirm:
                error = 'Пароли не совпадают'
            else:
                pwd_hash = generate_password_hash(new_password)

        if not error:
            if new_password:
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute("UPDATE users SET name=%s, password=%s WHERE id=%s;",
                                (new_name, pwd_hash, user['id']))
                else:
                    cur.execute("UPDATE users SET name=?, password=? WHERE id=?;",
                                (new_name, pwd_hash, user['id']))
            else:
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute("UPDATE users SET name=%s WHERE id=%s;",
                                (new_name, user['id']))
                else:
                    cur.execute("UPDATE users SET name=? WHERE id=?;",
                                (new_name, user['id']))

            db_close(conn, cur)
            return redirect('/lab5/profile')

    db_close(conn, cur)
    return render_template('lab5/profile.html', user=user, error=error)

@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.title, a.article_text, a.is_favorite, u.login, u.name
            FROM articles a JOIN users u ON a.user_id = u.id
            WHERE a.is_public = TRUE
            ORDER BY a.is_favorite DESC, a.id DESC;
        """)
    else:
        cur.execute("""
            SELECT a.title, a.article_text, a.is_favorite, u.login, u.name
            FROM articles a JOIN users u ON a.user_id = u.id
            WHERE a.is_public = 1
            ORDER BY a.is_favorite DESC, a.id DESC;
        """)

    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)