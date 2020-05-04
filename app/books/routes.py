import os
from flask import Blueprint, session, jsonify, render_template, request, redirect, url_for, jsonify, current_app
from werkzeug.utils import secure_filename
from .forms import BookForm
import firestore
from datetime import datetime
import storage



bp = Blueprint('books', __name__)

def clean_form_data(data):
    if 'csrf_token' in data:
        del data['csrf_token']
    if 'submit' in data:
        del data['submit']
    return data

def upload_image_file(img):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not img:
        return None

    public_url = storage.upload_file(
        img.read(),
        img.filename,
        img.content_type
    )

    current_app.logger.info(
        'Uploaded file %s as %s.', img.filename, public_url)
    print(f'public_url: {public_url}')
    return public_url


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
def add_book():
    """Load BookForm to add a book to the database"""
   
    form = BookForm()

    if form.validate_on_submit():
        data = clean_form_data(form.data)
        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files.get('cover_img'))
        if image_url != None:
            data['cover_img'] = image_url
        else:
            data['cover_img'] = ''
        book = firestore.create(data)
        return redirect(url_for('books.book_view', book_id=book['id']))
    return render_template('book_form.html', form=form, book={})


@bp.route('/update/<book_id>', methods=['GET', 'POST'])
def update(book_id):
    """Load BookForm with book information to edit book information in the database"""
    book = firestore.read(book_id, False)
    form = BookForm(data=book)

    if form.validate_on_submit():
        data = clean_form_data(form.data)
        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files.get('cover_img'))
        if image_url != None:
            data['cover_img'] = image_url
        else:
            data['cover_img'] = book['cover_img']
        book = firestore.update(clean_form_data(data), book['id'])
        return redirect(url_for('books.book_view', book_id=book['id']))
    if book['cover_img'] != '':
        book['cover_img'] = book['cover_img'].rsplit('/', 1)[1]
    return render_template('book_form.html', form=form, book=book)


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

@bp.route('/delete_cover', methods=['POST'])
def delete_cover():
    book_id = request.form.get('book_id')

    book = firestore.read(book_id)

    cover_filename = book['cover_img'].rsplit('/', 1) [1]

    firestore.delete_cover(book_id)
    storage.delete_cover(cover_filename)
    return jsonify('')
    #return redirect(url_for('books.book_view', book_id=book_id))


@bp.route('/test_post', methods=['POST'])
def test_post():
    book_id = request.form.get('book_id')
    print(book_id)
    return jsonify('')
    