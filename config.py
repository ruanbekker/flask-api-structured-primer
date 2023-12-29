import os

class Config(object):
    """Base configuration class."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    """Configuration class for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Configuration class for dev.

    Activated with FLASK_ENV=development
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    """
    Configuration class for dev.

    Activated with FLASK_ENV=production
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False