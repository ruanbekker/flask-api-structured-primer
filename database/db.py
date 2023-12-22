from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""The SQLAlchemy object for database management."""

def reset_database():
    """
    Reset the database by dropping all tables and recreating them.
    """
    db.drop_all()
    db.create_all()
