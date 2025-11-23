import pytest
from app import create_app, db


@pytest.fixture
def app_context():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app_context):
    return app_context.test_client()


def test_register_page_loads(client):
    response = client.get('/register')
    assert response.status_code == 200


def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200

