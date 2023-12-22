import os

class Config(object):
    """
    Base configuration class.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+mysqlconnector://user:password@localhost/db_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    """
    Configuration class for testing.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'