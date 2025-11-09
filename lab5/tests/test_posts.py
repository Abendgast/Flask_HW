import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def client():
    app = create_app('testing')
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_post(client):
    response = client.post('/posts/create', data={'title': 'Test', 'content': 'Content'}, follow_redirects=True)
    assert b'Post created successfully' in response.data

def test_post_list(client):
    response = client.get('/posts')
    assert response.status_code == 200

