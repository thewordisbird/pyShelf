import os

class Config:
    SECRET_KEY = os.environ.get('SECEET_KEY') or 'my_secret_key'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
