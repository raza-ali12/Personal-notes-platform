import pytest
import json

def test_register_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    
    assert response.status_code == 201
    data = response.json
    assert 'id' in data
    assert data['email'] == 'test@example.com'
    assert 'password' not in data

def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    # Register first user
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    
    # Try to register with same email
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'anotherpassword123'
    })
    
    assert response.status_code == 409
    assert 'already exists' in response.json['error']

def test_register_invalid_data(client):
    """Test registration with invalid data"""
    # Missing email
    response = client.post('/api/auth/register', json={
        'password': 'testpassword123'
    })
    assert response.status_code == 400
    
    # Invalid email format
    response = client.post('/api/auth/register', json={
        'email': 'invalid-email',
        'password': 'testpassword123'
    })
    assert response.status_code == 400
    
    # Short password
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': '123'
    })
    assert response.status_code == 400

def test_login_success(client):
    """Test successful login"""
    # Register user first
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    
    # Login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    
    assert response.status_code == 200
    data = response.json
    assert 'access_token' in data
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    # Register user first
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    
    # Wrong password
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    
    # Non-existent user
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'testpassword123'
    })
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    """Test getting current user information"""
    response = client.get('/api/auth/me', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert 'id' in data
    assert data['email'] == 'test@example.com'

def test_get_current_user_no_token(client):
    """Test getting current user without token"""
    response = client.get('/api/auth/me')
    assert response.status_code == 401
