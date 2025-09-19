from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def init_db(app):
    """Initialize database with app context"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

def hash_password(password):
    """Hash a password for storing"""
    return generate_password_hash(password)

def check_password(password_hash, password):
    """Check if provided password matches the hash"""
    return check_password_hash(password_hash, password)
