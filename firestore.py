import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import current_app

# For Cloud Deployed App:
#cred = credentials.ApplicationDefault()
# For Locally Deployed App:
#cred = credentials.Certificate('/Users/justinbird/Code/GCP_Keys/py-firestore-ebc03-local.json')
#cred = credentials.Certificate(app.config('FIRESTORE_CREDENTIALS'))
#firebase_admin.initialize_app(cred, {'project': 'py-firestore-ebc03'})

class Firestore:
    def __init__(self):
        self.name = 'Justin'
        if current_app.config['FIREBASE_LOCAL_KEY']:
            self.cred = credentials.Certificate(current_app.config['FIREBASE_LOCAL_KEY'])
        else:
            self.cred = credentials.ApplicationDefault()

        firebase_admin.initialize_app(self.cred, current_app.config['FIREBASE_PROJECT'])    

        self.client = firestore.client()

    def document_to_dict(self, doc):
        """Convert a Firestore document to dictionary"""
        if not doc.exists:
            return None
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id
        return doc_dict

    def create(self, data, collection, doc_id=None):
        doc_ref = self.client.collection(collection).document(doc_id)
        doc_ref.set(data)
        # Return the book info as a dictionary to be used in the redirect to the
        # book info page. 
        return self.document_to_dict(doc_ref.get())

    update = create

    def read_doc(self, collection, doc_id):
        doc_ref = self.client.collection(collection).document(doc_id)
        doc = doc_ref.get()
        return self.document_to_dict(doc)

    def read_all(self, collection, order_by):
        query = self.client.collection(collection).order_by(order_by)
        docs = query.stream()
        docs = list(map(self.document_to_dict, docs))
        return docs

    def read_limit(self, collection, order_by, start_after_key, start_after_val=None, limit=None):
        if limit == None:
            limit = current_app.config['PAGE_LIMIT']
        collection_ref = db.collection(collection)
        query =collection_ref.limit(limit).order_by(order_by)
        
        if start_after_val:
            # Construct a new query starting at given document
            query = query.start_after({start_after_key:start_after_val})
        
        docs = query.stream()
        docs = list(map(self.document_to_dict, docs))

        last_doc = None
        if limit == len(docs):
            # Get the last document from the results and set as the last title.
            last_doc = docs[-1][start_after_key]
        return docs, last_doc

    def delete(self, collection, doc_id):
        doc_ref = db.collection(collection).document(doc_id)
        doc_ref.delete()
     
    