import pytest
from datetime import datetime
from flask import current_app, session, template_rendered
from contextlib import contextmanager
from app import create_app
from config import TestingConfig
from app.books import forms
from dotenv import load_dotenv, find_dotenv

# Load enviornment and flask system variables
load_dotenv(find_dotenv())

@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        
        yield app
    # Run any builds requireing app_context

    # yield the app instance for use in test functions

@pytest.fixture()
def client(app):
    with app.test_request_context():
        with app.test_client() as client:
            yield client

def test_config(app):
    assert app.config['TESTING'] == True

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, Flask!'

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

# ========== Firestore Module Tests ==========
@pytest.fixture()
def fs(app):
    with current_app.app_context():
        import firestore
    # Capture current books
    books = firestore.read_all()

    # Pass firestore module
    yield firestore

    # Remove Test books (This is slow! For production It would be better to set up
    # a test project.)

    new_books = firestore.read_all()
    for book in new_books:
        if book not in books:
            firestore.delete(book['id'])

def test_firestore_create(fs):
    test_data = {
        'title': 'Test Title',
        'author': 'Test Author',
        'publication_date': datetime(2020, 2, 13),
        'description': 'Test Description'
    }

    doc = fs.create(test_data)
    assert doc['title'] == 'Test Title'


def test_firestore_update(fs):
    test_data = {
        'title': 'Test Title',
        'author': 'Test Author',
        'publication_date': datetime(2020, 2, 13),
        'description': 'Test Description'
    }

    doc = fs.create(test_data)
    update_data = {
        'title': 'Update Title',
        'author': 'Test Author',
        'publication_date': datetime(2020, 2, 13),
        'description': 'Test Description'
    }

    update = fs.update(update_data, doc['id'])
    assert update['title'] == 'Update Title'
    assert update['id'] == doc['id']


# ========== books/routes tests ==========
@pytest.fixture
def books(fs):
    
    for i in range(65,91):
        book = {
            'title': 'Test Title ' + chr(i),
            'author': 'Test Author ' + chr(i)
        }

        fs.create(book)
        
def test_index_handle_load(app, client, books):
    with captured_templates(app) as templates:
        rv = client.get('/')
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == "index.html"
        print(context)
        assert len(context['books']) == 10
        assert session['last_title'] == 'Test Title J'

def test_index_handle_ajax(app, client, books):
    last_title = 'Test Title J'
    with client.session_transaction() as sess:
        sess['last_title'] = last_title
    
    rv = client.post('/')
    assert rv.status_code == 200
    assert session['last_title'] == 'Test Title T'

def test_add_handle_load(app, client):
    """Upon a get request from the client. Confirm page loads"""
    with captured_templates(app) as templates:
        rv = client.get('/add')
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'book_form.html'


def test_add_handle_form_submit(client, fs):
    """Process post request to add book to database"""
    data ={
        'title': 'Test Title',
        'author': 'Test Author',
        'publication_date': datetime(2020, 2, 13).strftime('%m/%d/%Y'),
        'description': 'Test Description'
    }
    form = forms.BookForm(data=data)
    #print(form.data)
    
    rv = client.post('/add', data=form.data, follow_redirects=False)
    assert rv.status == '302 FOUND'
    
    # Check that book is in firestore DB
    db = fs.firestore.client()
    docs = db.collection('Book').where('title', '==', 'Test Title').stream()
    books = list(map(fs.document_to_dict, docs))
    assert len(books) == 1
    book = books[0]
    assert book['title'] == data['title']
    
def test_update_handle_load(app, client, fs):
    data ={
        'title': 'Test Title',
        'author': 'Test Author',
        'publication_date': datetime(2020, 2, 13),
        'description': 'Test Description'
    }

    book = fs.create(data)
    with captured_templates(app) as templates:
        rv = client.get('/update/' + book['id'])
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'book_form.html'
        print(context)
        assert context['form'].data['title'] == 'Test Title'
    
    fs.delete(book['id'])

def test_update_handle_form_submit(client, fs):
    data ={
        'title': 'Test Title',
        'author': 'Test Author',
        'publication_date': datetime(2020, 2, 13),
        'description': 'Test Description'
    }

    book = fs.format_time(fs.create(data))

    # Modify book data and populate form data
    book['title'] = 'Test Title Updated'
    form = forms.BookForm(data=book)
    print('/update/'+book['id'])
    rv = client.post('/update/'+book['id'], data=form.data, follow_redirects=False)
    print(rv.status)
    assert rv.status == '302 FOUND'

    # Check book is updated in firestore DB
    book = fs.read(book['id'])
    assert book['title'] == 'Test Title Updated'


def test_book_view_handle_load(app, client, fs):
    data ={
        'title': 'Test Title',
        'author': 'Test Author',
        'publication_date': datetime(2020, 2, 13),
        'description': 'Test Description'
    }

    book = fs.create(data)
    with captured_templates(app) as templates:
        rv = client.get('/book/' + book['id'])
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'book_view.html'
        assert context['book']['title'] == 'Test Title'
    
    fs.delete(book['id'])

def test_delete_handle_request(app, client, fs):
    data ={
        'title': 'Test Title',
        'author': 'Test Author',
        'publication_date': datetime(2020, 2, 13),
        'description': 'Test Description'
    }

    book = fs.create(data)
    rv = client.get('/delete/'+book['id'])
    assert rv.status == '302 FOUND'
    assert fs.read(book['id']) == None

        