"""Product Service."""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from database.db import db
from models.product import Product
from services.product_service import ProductService
from views.product_views import product_blueprint

def create_app(config_class=Config):
    """
    Create a Flask application.

    Parameters:
    config_class (Config): The configuration class for the application.

    Returns:
    Flask: The Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Initialize Migrate
    migrate = Migrate(app, db)

    # Register routes
    app.register_blueprint(product_blueprint, url_prefix='/api')

    return app