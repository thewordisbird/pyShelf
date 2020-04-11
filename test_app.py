import pytest

from app import create_app
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)

    # Run any builds requireing app_context

    # yield the app instance for use in test functions
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_config():
    assert create_app().testing == False
    assert create_app(TestingConfig).testing == True
    
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, Flask!'