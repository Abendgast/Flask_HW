from app import db
from app.models import User


def test_register_user(client, app_context):
    response = client.post('/register', data={
        "username": "john",
        "email": "john@example.com",
        "password": "secret123",
        "confirm": "secret123"
    }, follow_redirects=True)

    assert b"Registration successful" in response.data
    assert User.query.count() == 1


def test_login_logout(client, app_context):
    u = User(username="alex", email="alex@example.com")
    u.set_password("pass123")
    db.session.add(u)
    db.session.commit()

    response = client.post('/login', data={
        "email": "alex@example.com",
        "password": "pass123"
    }, follow_redirects=True)

    assert b"Profile" in response.data

    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data

