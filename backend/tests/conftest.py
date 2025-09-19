import pytest
import tempfile
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from db import db, init_db

@pytest.fixture(scope='function')
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to serve as the database
    db_fd, db_path = tempfile.mkstemp()
    
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'JWT_SECRET_KEY': 'test-jwt-secret-key',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_ACCESS_TOKEN_EXPIRES': 86400,
        'CORS_ORIGINS': ['http://localhost:5173']
    })
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.notes import notes_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(notes_bp, url_prefix='/api/notes')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}
    
    with app.app_context():
        init_db(app)
        yield app
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def auth_headers(client, app):
    """Get authentication headers for testing."""
    # Register a test user
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    assert response.status_code == 201
    
    # Login to get token
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    assert response.status_code == 200
    
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}
