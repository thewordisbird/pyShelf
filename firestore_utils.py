import firestore
from datetime import datetime

BOOKS = [
    {
        "author": "Amor Towles",
        "cover_img": "https://storage.googleapis.com/pyshself.appspot.com/gim-2020-05-04-001712.jpeg",
        "description": "Great Book",
        "publication_date": datetime.now(),
        "title": "A Gentleman in Moscow"
    },
    {
        "author": "Steven King",
        "cover_img": "https://storage.googleapis.com/pyshself.appspot.com/gim-2020-05-04-001712.jpeg",
        "description": "Great Book",
        "publication_date": datetime.now(),
        "title": "A Gentleman in Moscow"
    }
]

def delete_all_docs():
    docs = firestore.read_all()

    confirm = input("This will delete all books. Continue (y/n): ")
    if confirm == 'y':
        count = 0
        for doc in docs:
            count += 1
            firestore.delete(doc['id'])
        print(f'{count} books have been deleted')


def add_books():
    count = 0
    for book in BOOKS:
        count += 1
        firestore.create(book)
    print(f'Added {count} books to the database')
    