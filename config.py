import os

class Config(object):
    """Base configuration class."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+mysqlconnector://user:password@localhost/product_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    """Configuration class for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class SwaggerConfig:
    """Configuration class for Swagger."""
    TITLE = "Product Service API"
    SPECS = [
        {
            "version": "1.0",
            "title": TITLE,
            "endpoint": "apispec_1",
            "route": "/apispec_1.json"
        }
    ]
    HEADERS = []
    STATIC_URL_PATH = "/flasgger_static"
    SWAGGER_UI = True
    SPECS_ROUTE = "/apidocs/"

class DevelopmentConfig(Config):
    """
    Configuration class for dev.

    Activated with FLASK_ENV=development
    """

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://ruan:password@127.0.0.1/product_db'

class ProductionConfig(Config):
    """
    Configuration class for dev.

    Activated with FLASK_ENV=production
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False