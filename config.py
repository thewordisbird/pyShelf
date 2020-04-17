import os

class Config:
    SECRET_KEY = os.environ.get('SECEET_KEY') or 'my_secret_key'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    FIREBASE_LOCAL_KEY = './keys/pyshelf-firestore.json'
    FIREBASE_PROJECT = {'project': 'pyshself'}
    PAGE_LIMIT = 10

class TestingConfig(Config):
    TESTING = True
    FIREBASE_LOCAL_KEY = './keys/pyshelf-firestore.json'
    FIREBASE_PROJECT = {'project': 'pyshself'}
    PAGE_LIMIT = 10
    WTF_CSRF_ENABLED = False
