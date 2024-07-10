import hashlib
import sqlite3

from flask import current_app
from flask_login import UserMixin
from app import login_manager
from app.models import get_db

class User(UserMixin):
    def __init__(self, id_, username, password, role):
        self.id = id_
        self.username = username
        self.password = password
        self.role = role

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

def init_db():
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
);
        ''')
        db.commit()
