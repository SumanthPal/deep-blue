import pytest
from app import app

@pytest.fixture
def app_context():
    with app.app_context():
        app.init_db()
        yield
        app.get_db().execute('DROP TABLE IF EXISTS user')
        app.get_db().commit()

def test_user_model(app_context):
    db = app.get_db()
    db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
               ('testuser', 'password'))
    db.commit()
    user = db.execute("SELECT * FROM user WHERE username = ?", ('testuser',)).fetchone()
    assert user['username'] == 'testuser'
    assert user['password'] == 'password'
