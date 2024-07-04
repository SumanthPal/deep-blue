import os
import sqlite3
from flask import g, current_app

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(os.getenv('DATABASE_URL'))
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db_command():
    """Initialize the database with existing schema."""
    init_db()
    print('Initialized the database with existing schema.')

def add_db(name, address):
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO user(name, address) VALUES(?,?)", (name, address))
        db.commit()
def init_db():
    """Initialize database by creating necessary tables if they do not exist."""
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        db.commit()
