import pytest
import json

def test_create_note(client, auth_headers):
    """Test creating a new note"""
    response = client.post('/api/notes', 
        json={'title': 'Test Note', 'content': 'This is a test note'},
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json
    assert data['title'] == 'Test Note'
    assert data['content'] == 'This is a test note'
    assert 'id' in data
    assert 'user_id' in data
    assert 'created_at' in data

def test_create_note_no_auth(client):
    """Test creating a note without authentication"""
    response = client.post('/api/notes', 
        json={'title': 'Test Note', 'content': 'This is a test note'}
    )
    assert response.status_code == 401

def test_get_notes(client, auth_headers):
    """Test getting all notes for a user"""
    # Create a note first
    client.post('/api/notes', 
        json={'title': 'Test Note 1', 'content': 'Content 1'},
        headers=auth_headers
    )
    client.post('/api/notes', 
        json={'title': 'Test Note 2', 'content': 'Content 2'},
        headers=auth_headers
    )
    
    # Get all notes
    response = client.get('/api/notes', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert len(data) == 2
    assert data[0]['title'] == 'Test Note 2'  # Should be ordered by updated_at desc
    assert data[1]['title'] == 'Test Note 1'

def test_get_notes_no_auth(client):
    """Test getting notes without authentication"""
    response = client.get('/api/notes')
    assert response.status_code == 401

def test_get_single_note(client, auth_headers):
    """Test getting a single note"""
    # Create a note
    create_response = client.post('/api/notes', 
        json={'title': 'Test Note', 'content': 'Test content'},
        headers=auth_headers
    )
    note_id = create_response.json['id']
    
    # Get the note
    response = client.get(f'/api/notes/{note_id}', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert data['title'] == 'Test Note'
    assert data['content'] == 'Test content'

def test_get_nonexistent_note(client, auth_headers):
    """Test getting a note that doesn't exist"""
    response = client.get('/api/notes/999', headers=auth_headers)
    assert response.status_code == 404

def test_update_note(client, auth_headers):
    """Test updating a note"""
    # Create a note
    create_response = client.post('/api/notes', 
        json={'title': 'Original Title', 'content': 'Original content'},
        headers=auth_headers
    )
    note_id = create_response.json['id']
    
    # Update the note
    response = client.put(f'/api/notes/{note_id}', 
        json={'title': 'Updated Title', 'content': 'Updated content'},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json
    assert data['title'] == 'Updated Title'
    assert data['content'] == 'Updated content'

def test_update_note_partial(client, auth_headers):
    """Test partial update of a note"""
    # Create a note
    create_response = client.post('/api/notes', 
        json={'title': 'Original Title', 'content': 'Original content'},
        headers=auth_headers
    )
    note_id = create_response.json['id']
    
    # Update only title
    response = client.put(f'/api/notes/{note_id}', 
        json={'title': 'Updated Title Only'},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json
    assert data['title'] == 'Updated Title Only'
    assert data['content'] == 'Original content'  # Should remain unchanged

def test_delete_note(client, auth_headers):
    """Test deleting a note"""
    # Create a note
    create_response = client.post('/api/notes', 
        json={'title': 'To Delete', 'content': 'This will be deleted'},
        headers=auth_headers
    )
    note_id = create_response.json['id']
    
    # Delete the note
    response = client.delete(f'/api/notes/{note_id}', headers=auth_headers)
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f'/api/notes/{note_id}', headers=auth_headers)
    assert get_response.status_code == 404

def test_user_isolation(client, auth_headers):
    """Test that users can only access their own notes"""
    # Create a note with first user
    create_response = client.post('/api/notes', 
        json={'title': 'User 1 Note', 'content': 'Private content'},
        headers=auth_headers
    )
    note_id = create_response.json['id']
    
    # Register a second user
    client.post('/api/auth/register', json={
        'email': 'test2@example.com',
        'password': 'testpassword123'
    })
    
    # Login as second user
    login_response = client.post('/api/auth/login', json={
        'email': 'test2@example.com',
        'password': 'testpassword123'
    })
    user2_headers = {'Authorization': f"Bearer {login_response.json['access_token']}"}
    
    # Try to access first user's note
    response = client.get(f'/api/notes/{note_id}', headers=user2_headers)
    assert response.status_code == 404
    
    # Try to update first user's note
    response = client.put(f'/api/notes/{note_id}', 
        json={'title': 'Hacked Title'},
        headers=user2_headers
    )
    assert response.status_code == 404
    
    # Try to delete first user's note
    response = client.delete(f'/api/notes/{note_id}', headers=user2_headers)
    assert response.status_code == 404
