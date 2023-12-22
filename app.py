"""Product Service."""
import os
from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger
from config import Config, DevelopmentConfig, ProductionConfig
from database.db import db
from views.product_views import product_blueprint

def create_app(config_class=Config):
    """
    Create a Flask application.

    Parameters
    ----------
    config_class : Config, optional
        The configuration class for the application. Defaults to `Config`.

    Returns
    -------
    Flask
        The Flask application instance.
    """
    app = Flask(__name__)
    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object(DevelopmentConfig)
    elif os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Initialize Migrate
    Migrate(app, db)

    # Register routes
    app.register_blueprint(product_blueprint, url_prefix='/api')

    # Initialize Swagger
    swagger = Swagger(config={
        "title": SwaggerConfig.TITLE,
        "specs": SwaggerConfig.SPECS,
        "headers": SwaggerConfig.HEADERS,
        "static_url_path": SwaggerConfig.STATIC_URL_PATH,
        "swagger_ui": SwaggerConfig.SWAGGER_UI,
        "specs_route": SwaggerConfig.SPECS_ROUTE,
    })
    swagger.init_app(app)

    return app