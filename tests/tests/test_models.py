import pytest
import sqlite3

from app.models import get_db, init_db

@pytest.fixture
def init_database():
    app.config['TESTING'] = True
    init_db()
    db = get_db()
    yield db
    db.execute('DROP TABLE user')
    db.commit()

def test_user_model(init_database):
    """Test the User model"""
    db = init_database
    db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
               ('testuser', 'password'))
    db.commit()
    user = db.execute("SELECT * FROM user WHERE username = ?", ('testuser',)).fetchone()
    assert user['username'] == 'testuser'
    assert user['password'] == 'password'
