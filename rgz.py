from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import datetime
import os
import json
import random

rgz = Blueprint('rgz', __name__, url_prefix='/rgz')
DB_PATH = os.path.join(os.path.dirname(__file__), "rgz.db")

# --- Создание БД и таблиц ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Пользователи
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    
    # Инициативы
    c.execute('''
        CREATE TABLE IF NOT EXISTS initiatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            date TEXT NOT NULL,
            votes INTEGER DEFAULT 0,
            author_id INTEGER NOT NULL,
            FOREIGN KEY(author_id) REFERENCES users(id)
        )
    ''')
    
    # Голоса
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            initiative_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            vote INTEGER NOT NULL,
            FOREIGN KEY(initiative_id) REFERENCES initiatives(id),
            FOREIGN KEY(user_id) REFERENCES users(id),
            UNIQUE(initiative_id, user_id)
        )
    ''')
    
    # Создаем администратора если его нет
    admin = c.execute("SELECT * FROM users WHERE username='admin'").fetchone()
    if not admin:
        c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                 ('admin', generate_password_hash('admin123'), 1))
    
    # Создаем тестовые инициативы (более 100)
    init_count = c.execute("SELECT COUNT(*) FROM initiatives").fetchone()[0]
    if init_count < 100:
        users = c.execute("SELECT id FROM users").fetchall()
        if len(users) < 10:
            for i in range(10):
                try:
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                             (f'user{i}', generate_password_hash(f'pass{i}')))
                except:
                    pass
            users = c.execute("SELECT id FROM users").fetchall()
        
        titles = [
            "Улучшение системы отопления", "Ремонт дорог", "Озеленение территории",
            "Создание велодорожек", "Реконструкция парка", "Установка новых лавочек",
            "Организация культурных мероприятий", "Улучшение освещения улиц",
            "Строительство детской площадки", "Ремонт фасадов зданий"
        ]
        
        texts = [
            "Предлагаю улучшить систему отопления в зимний период",
            "Необходимо отремонтировать дороги в нашем районе",
            "Предлагаю организовать озеленение территории",
            "Создание велодорожек сделает наш город более современным",
            "Реконструкция парка улучшит качество отдыха горожан"
        ]
        
        for i in range(100 - init_count):
            title = random.choice(titles) + f" #{i+1}"
            text = random.choice(texts)
            year = 2024 if i % 3 == 0 else 2025
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date = f"{year}-{month:02d}-{day:02d} 00:00:00"
            author_id = random.choice(users)[0]
            votes = random.randint(-5, 20)
            c.execute("INSERT INTO initiatives (title, text, date, author_id, votes) VALUES (?, ?, ?, ?, ?)",
                     (title, text, date, author_id, votes))
    
    conn.commit()
    conn.close()

init_db()

# --- Вспомогательные функции ---
def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, password, is_admin FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_initiatives(page=1, per_page=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    offset = (page - 1) * per_page
    c.execute("SELECT i.id, i.title, i.text, i.date, i.votes, u.username "
              "FROM initiatives i JOIN users u ON i.author_id=u.id "
              "ORDER BY i.id DESC LIMIT ? OFFSET ?", (per_page, offset))
    initiatives = c.fetchall()
    conn.close()
    return initiatives

def get_user_initiatives(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, text, date, votes FROM initiatives WHERE author_id = ? ORDER BY id DESC", (user_id,))
    initiatives = c.fetchall()
    conn.close()
    return initiatives

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, is_admin FROM users ORDER BY id")
    users = c.fetchall()
    conn.close()
    return users

# --- JSON-RPC API ---
class JSONRPCException(Exception):
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data

def jsonrpc_response(result=None, error=None, id=None):
    response = {"jsonrpc": "2.0", "id": id}
    if error:
        response["error"] = error
    else:
        response["result"] = result
    return jsonify(response)

def handle_jsonrpc_request():
    if request.method != 'POST':
        return jsonrpc_response(error={"code": -32600, "message": "Invalid Request"})
    
    try:
        data = request.get_json()
        if not data:
            return jsonrpc_response(error={"code": -32700, "message": "Parse error"})
        
        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id')
        
        if method == 'register':
            result = api_register(params)
        elif method == 'login':
            result = api_login(params)
        elif method == 'logout':
            result = api_logout()
        elif method == 'get_initiatives':
            result = api_get_initiatives(params)
        elif method == 'create_initiative':
            result = api_create_initiative(params)
        elif method == 'delete_initiative':
            result = api_delete_initiative(params)
        elif method == 'vote':
            result = api_vote(params)
        elif method == 'get_my_initiatives':
            result = api_get_my_initiatives()
        elif method == 'get_users':
            result = api_get_users()
        elif method == 'delete_user':
            result = api_delete_user(params)
        elif method == 'delete_initiative_admin':
            result = api_delete_initiative_admin(params)
        else:
            raise JSONRPCException(-32601, "Method not found")
        
        return jsonrpc_response(result=result, id=request_id)
    
    except JSONRPCException as e:
        return jsonrpc_response(error={"code": e.code, "message": e.message, "data": e.data}, id=request_id)
    except Exception as e:
        return jsonrpc_response(error={"code": -32603, "message": "Internal error", "data": str(e)}, id=request_id)

# --- API методы ---
def api_register(params):
    username = params.get('username')
    password = params.get('password')
    
    if not username or not password:
        raise JSONRPCException(-32602, "Invalid params", "Username and password required")
    
    if get_user_by_username(username):
        raise JSONRPCException(-32000, "User already exists")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?,?)",
              (username, generate_password_hash(password)))
    conn.commit()
    conn.close()
    
    return {"message": "User registered successfully"}

def api_login(params):
    username = params.get('username')
    password = params.get('password')
    
    if not username or not password:
        raise JSONRPCException(-32602, "Invalid params", "Username and password required")
    
    user = get_user_by_username(username)
    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['is_admin'] = bool(user[3])
        return {"message": "Login successful", "user": {"username": user[1], "is_admin": bool(user[3])}}
    
    raise JSONRPCException(-32001, "Invalid credentials")

def api_logout():
    session.clear()
    return {"message": "Logout successful"}

def api_get_initiatives(params):
    page = params.get('page', 1)
    initiatives = get_initiatives(page)
    
    result = []
    for init in initiatives:
        result.append({
            'id': init[0],
            'title': init[1],
            'text': init[2],
            'date': init[3],
            'votes': init[4],
            'author': init[5]
        })
    
    return {"initiatives": result, "has_more": len(get_initiatives(page + 1)) > 0}

def api_create_initiative(params):
    if 'user_id' not in session:
        raise JSONRPCException(-32002, "Authentication required")
    
    title = params.get('title')
    text = params.get('text')
    
    if not title or not text:
        raise JSONRPCException(-32602, "Invalid params", "Title and text required")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO initiatives (title, text, date, author_id) VALUES (?,?,?,?)",
              (title, text, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), session['user_id']))
    conn.commit()
    conn.close()
    
    return {"message": "Initiative created successfully"}

def api_delete_initiative(params):
    if 'user_id' not in session:
        raise JSONRPCException(-32002, "Authentication required")
    
    init_id = params.get('id')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT author_id FROM initiatives WHERE id = ?", (init_id,))
    initiative = c.fetchone()
    
    if not initiative:
        conn.close()
        raise JSONRPCException(-32003, "Initiative not found")
    
    if initiative[0] != session['user_id'] and not session.get('is_admin'):
        conn.close()
        raise JSONRPCException(-32004, "Permission denied")
    
    c.execute("DELETE FROM initiatives WHERE id = ?", (init_id,))
    c.execute("DELETE FROM votes WHERE initiative_id = ?", (init_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Initiative deleted successfully"}

def api_vote(params):
    if 'user_id' not in session:
        raise JSONRPCException(-32002, "Authentication required")
    
    init_id = params.get('initiative_id')
    vote_type = params.get('type')
    
    if vote_type not in ['up', 'down']:
        raise JSONRPCException(-32602, "Invalid params", "Vote type must be 'up' or 'down'")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT id FROM initiatives WHERE id = ?", (init_id,))
    if not c.fetchone():
        conn.close()
        raise JSONRPCException(-32003, "Initiative not found")
    
    c.execute("SELECT vote FROM votes WHERE initiative_id = ? AND user_id = ?", (init_id, session['user_id']))
    existing_vote = c.fetchone()
    
    vote_val = 1 if vote_type == 'up' else -1
    
    if existing_vote:
        old_vote = existing_vote[0]
        c.execute("UPDATE votes SET vote = ? WHERE initiative_id = ? AND user_id = ?", 
                 (vote_val, init_id, session['user_id']))
        c.execute("UPDATE initiatives SET votes = votes - ? + ? WHERE id = ?", 
                 (old_vote, vote_val, init_id))
    else:
        c.execute("INSERT INTO votes (initiative_id, user_id, vote) VALUES (?, ?, ?)", 
                 (init_id, session['user_id'], vote_val))
        c.execute("UPDATE initiatives SET votes = votes + ? WHERE id = ?", (vote_val, init_id))
    
    c.execute("DELETE FROM initiatives WHERE votes < -10")
    conn.commit()
    conn.close()
    
    return {"message": "Vote recorded successfully"}

def api_get_my_initiatives():
    if 'user_id' not in session:
        raise JSONRPCException(-32002, "Authentication required")
    
    initiatives = get_user_initiatives(session['user_id'])
    result = []
    for init in initiatives:
        result.append({
            'id': init[0],
            'title': init[1],
            'text': init[2],
            'date': init[3],
            'votes': init[4]
        })
    
    return {"initiatives": result}

def api_get_users():
    if not session.get('is_admin'):
        raise JSONRPCException(-32004, "Admin access required")
    
    users = get_all_users()
    result = []
    for user in users:
        result.append({
            'id': user[0],
            'username': user[1],
            'is_admin': bool(user[2])
        })
    
    return {"users": result}

def api_delete_user(params):
    if not session.get('is_admin'):
        raise JSONRPCException(-32004, "Admin access required")
    
    user_id = params.get('id')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if user_id == session['user_id']:
        conn.close()
        raise JSONRPCException(-32005, "Cannot delete your own account")
    
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    c.execute("DELETE FROM initiatives WHERE author_id = ?", (user_id,))
    c.execute("DELETE FROM votes WHERE user_id = ?", (user_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "User deleted successfully"}

def api_delete_initiative_admin(params):
    if not session.get('is_admin'):
        raise JSONRPCException(-32004, "Admin access required")
    
    init_id = params.get('id')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("DELETE FROM initiatives WHERE id = ?", (init_id,))
    c.execute("DELETE FROM votes WHERE initiative_id = ?", (init_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "Initiative deleted successfully"}

# --- Маршруты ---
@rgz.route('/api', methods=['POST'])
def rgz_api():
    return handle_jsonrpc_request()

@rgz.route('/')
def rgz_index():
    return render_template('rgz/rgz.html')

@rgz.route('/admin')
def rgz_admin():
    if not session.get('is_admin'):
        return redirect(url_for('rgz.rgz_index'))
    return render_template('rgz/admin.html')
