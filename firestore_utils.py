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
        "author": "Steve Erickson",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "Rubicon Beach: A Novel"
    },
    {
        "author": "Erin Morgenstern",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "The Starless Sea"
    },
    {
        "author": "Douglas Adams",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "The Hitchhiker's Guide to the Galaxy"
    },
    {
        "author": "Jami Attenberg",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "All This Could Be Yours"
    },
    {
        "author": "Charles Bukowski",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "Ham on Rye"
    },
    {
        "author": "Ocean Vuong",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "On Earth We're Briefly Georgous"
    },
    {
        "author": "Salman Khan",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "The One World School House"
    },
    {
        "author": "Delia Owens",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "Where the Crawdads Sing"
    },
    {
        "author": "Mohsin Hamid",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "How to Get Filthy Rich in Rising Asia"
    },
    {
        "author": "Elliot Ackerman",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "Waiting For Eden"
    },
    {
        "author": "Margaret Atwood",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "The Handmaid's Tale"
    },
    {
        "author": "Ray Bradbury",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "Farenheit 451"
    },
    {
        "author": "Dennis Lehane",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "Mystic River"
    },
    {
        "author": "Colson Whitehead",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "The Nickle Boys"
    },
    {
        "author": "Susan Orlean",
        "cover_img": "",
        "description": "",
        "publication_date": datetime.now(),
        "title": "The Library Book"
    },
    
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
    