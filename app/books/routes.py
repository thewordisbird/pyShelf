from flask import Blueprint, session, jsonify, render_template, request, redirect, url_for, jsonify
from .forms import BookForm, LoginForm
import firestore
from datetime import datetime



bp = Blueprint('books', __name__)

def clean_form_data(data):
    if 'csrf_token' in data:
        del data['csrf_token']
    if 'submit' in data:
        del data['submit']
    return data


@bp.route('/', methods=['GET', 'POST'])
def index():
    """Load feed of all books for user
    
    Handles AJAX POST requests for pagination
    """
    if request.method == 'POST':
        # Handle AJAX request for more titles
        if session['last_title'] != None:
            books, session['last_title'] = firestore.read_limit(start_after=session['last_title'])
            return jsonify(books)
        return jsonify(None)
    else:
        # Handle initial page load
        books, session['last_title'] = firestore.read_limit()
        return render_template('index.html', books=books)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    """Load BookForm to add a book to the database"""
    print('Im HERE')
    form = BookForms()
    
    print(request.form.to_dict())
    print(form.is_submitted(), form.validate(), form.errors)
  
    if form.validate_on_submit():
        book = firestore.create(clean_form_data(form.data))

        # Upload image to google cloud store
        #image_url = upload_image_file(request.files.get('image'))

        # Redirect to book view page
        return redirect(url_for('books.book_view', book_id=book['id']))
    return render_template('book_form.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template('login.html', form=form)


@bp.route('/update/<book_id>', methods=['GET', 'POST'])
def update(book_id):
    """Load BookForm with book information to edit book information in the database"""
    book = firestore.read(book_id, False)
    form = BookForm(data=book)

    if form.validate_on_submit():
        book = firestore.update(clean_form_data(form.data), book['id'])
        return redirect(url_for('books.book_view', book_id=book['id']))
    return render_template('book_form.html', form=form)


@bp.route('/book/<book_id>', methods=['GET'])
def book_view(book_id):
    """Load page to view induvidual book information"""
    book = firestore.read(book_id)
    return render_template('book_view.html', book=book)


@bp.route('/delete/<book_id>', methods=['GET'])
def delete(book_id):
    """Delete the book from the database"""
    firestore.delete(book_id)
    return redirect(url_for('books.index'))


    