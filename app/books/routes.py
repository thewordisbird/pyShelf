from flask import Blueprint, session, jsonify, render_template, request, redirect, url_for
import firestore

from .forms import BookForm

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
    form = BookForm()

    if form.validate_on_submit():
        book = firestore.create(clean_form_data(form.data))
        # Redirect to book view page
        return redirect(url_for('books.book_view', book_id=book['id']))
    return render_template('book_form.html', form=form)

@bp.route('/update/<book_id>', methods=['GET', 'POST'])
def update(book_id):
    print('in update')
    book = firestore.read(book_id)
    form = BookForm(data=book)

    if form.validate_on_submit():
        print('validating')
        book = firestore.update(clean_form_data(form.data), book['id'])
        return redirect(url_for('books.book_view', book_id=book['id']))
    return render_template('book_form.html', form=form)


@bp.route('/book/<book_id>', methods=['GET'])
def book_view(book_id):
    book = firestore.read(book_id)
    return render_template('book_view.html', book=book)





    