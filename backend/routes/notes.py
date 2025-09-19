from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from db import db
from models import Note
from schemas import note_schema, notes_schema, note_update_schema

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('', methods=['GET'])
@jwt_required()
def get_notes():
    """Get all notes for the current user"""
    user_id = int(get_jwt_identity())
    notes = Note.query.filter_by(user_id=user_id).order_by(Note.updated_at.desc()).all()
    
    return jsonify(notes_schema.dump(notes)), 200

@notes_bp.route('', methods=['POST'])
@jwt_required()
def create_note():
    """Create a new note"""
    try:
        data = note_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'details': err.messages}), 400
    
    user_id = int(get_jwt_identity())
    
    note = Note(
        title=data['title'],
        content=data.get('content', ''),
        user_id=user_id
    )
    
    db.session.add(note)
    db.session.commit()
    
    return jsonify(note_schema.dump(note)), 201

@notes_bp.route('/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    """Get a specific note by ID"""
    user_id = int(get_jwt_identity())
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    return jsonify(note_schema.dump(note)), 200

@notes_bp.route('/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    """Update a specific note by ID"""
    try:
        data = note_update_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'details': err.messages}), 400
    
    user_id = int(get_jwt_identity())
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Update fields if provided
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    
    db.session.commit()
    
    return jsonify(note_schema.dump(note)), 200

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    """Delete a specific note by ID"""
    user_id = int(get_jwt_identity())
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    db.session.delete(note)
    db.session.commit()
    
    return '', 204
