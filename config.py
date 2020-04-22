import os

class Config:
    SECRET_KEY = os.environ.get("SECEET_KEY") or 'my_secret_key'
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    FIREBASE_KEY_URL = os.environ.get('FIREBASE_KEY_URL')
    FIREBASE_PROJECT = os.environ.get('FIREBASE_PROJECT')
    PAGINATION_LIMIT = os.environ.get('PAGINATION_LIMIT') or 10
    WTF_CSRF_ENABLED = True

class TestingConfig(Config):
    TESTING = True
    FIREBASE_KEY_URL = os.environ.get('FIREBASE_KEY_URL')
    FIREBASE_PROJECT = os.environ.get('FIREBASE_PROJECT')
    PAGINATION_LIMIT = os.environ.get('PAGINATION_LIMIT') or 10
    WTF_CSRF_ENABLED = False
