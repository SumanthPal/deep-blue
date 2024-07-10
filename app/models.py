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

def increment_frequency(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT frequency FROM frequency WHERE user_id = ?', (id,))
    result = cursor.fetchone()

    if result:
        new_frequency = result[0] + 1
        cursor.execute('UPDATE frequency SET frequency = ? WHERE user_id = ?', (new_frequency, id))
        db.commit()
    else:
        cursor.execute('INSERT INTO frequency (user_id, frequency) VALUES (?, ?)', (id, 1))
        db.commit()

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

        # Insert user into user table
        cursor.execute("INSERT INTO user(name, address) VALUES (?, ?)", (name, address))
        db.commit()

        # Retrieve the user ID of the newly inserted user
        cursor.execute("SELECT id FROM user WHERE name=?", (name,))
        user_id = cursor.fetchone()[0]

        # Insert initial frequency into frequency table
        cursor.execute("INSERT INTO frequency(user_id, frequency) VALUES (?, ?)", (user_id, 1))
        db.commit()

def delete_db(name):
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Get the user ID from the user table
        cursor.execute('SELECT id FROM user WHERE name = ?', (name,))
        user_id = cursor.fetchone()

        if user_id:
            # Delete from frequency table
            cursor.execute('DELETE FROM frequency WHERE user_id = ?', (user_id[0],))

            # Delete from user table
            cursor.execute('DELETE FROM user WHERE name = ?', (name,))

        db.commit()

def init_db():
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                UNIQUE(name)  -- Ensure name is unique in user table
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS frequency (
                user_id INTEGER PRIMARY KEY,
                frequency INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        ''')
        db.commit()
