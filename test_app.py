import pytest
from datetime import date
from app import create_app
from firestore import Firestore
from config import TestingConfig

@pytest.fixture(scope='module')
def app():
    app = create_app(TestingConfig)

    # Run any builds requireing app_context

    # yield the app instance for use in test functions
    yield app

@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        yield client

def test_config(app):
    assert app.config['TESTING'] == True
    
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, Flask!'

# ========== Firestore Module Tests ==========
@pytest.fixture(scope='module')
def fs(app):
    with app.app_context():
        return Firestore()

def clean_books(func):
    def wrapper():
        # Run test function
        book = func()
        # Compare databse changes and 

def test_firestore_construction(fs):
    assert fs.cred is not None


def test_firestore_create(fs):
    test_data = {
        'title': 'Test Title',
        'author': 'Test Author',
        'publication_date': "11/13/1984",
        'description': 'Test Description'
    }

    doc = fs.create(test_data, 'Books')
    assert doc['title'] == 'Test Title'
