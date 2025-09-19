import { useState, useEffect } from 'react'
import api from '../api/axios'
import NoteForm from '../components/NoteForm'
import NoteItem from '../components/NoteItem'

const Notes = () => {
  const [notes, setNotes] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isCreating, setIsCreating] = useState(false)
  const [editingNote, setEditingNote] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Fetch notes on component mount
  useEffect(() => {
    fetchNotes()
  }, [])

  const fetchNotes = async () => {
    try {
      setIsLoading(true)
      const response = await api.get('/notes')
      setNotes(response.data)
    } catch (error) {
      setError('Failed to fetch notes')
      console.error('Error fetching notes:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateNote = async (formData) => {
    try {
      setIsCreating(true)
      setError('')
      const response = await api.post('/notes', formData)
      setNotes(prev => [response.data, ...prev])
      setSuccess('Note created successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (error) {
      setError('Failed to create note')
      console.error('Error creating note:', error)
    } finally {
      setIsCreating(false)
    }
  }

  const handleEditNote = (note) => {
    setEditingNote(note)
  }

  const handleUpdateNote = async (formData) => {
    try {
      setError('')
      const response = await api.put(`/notes/${editingNote.id}`, formData)
      setNotes(prev => 
        prev.map(note => 
          note.id === editingNote.id ? response.data : note
        )
      )
      setEditingNote(null)
      setSuccess('Note updated successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (error) {
      setError('Failed to update note')
      console.error('Error updating note:', error)
    }
  }

  const handleDeleteNote = async (noteId) => {
    try {
      await api.delete(`/notes/${noteId}`)
      setNotes(prev => prev.filter(note => note.id !== noteId))
      setSuccess('Note deleted successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (error) {
      setError('Failed to delete note')
      console.error('Error deleting note:', error)
    }
  }

  const handleCancelEdit = () => {
    setEditingNote(null)
  }

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading notes...</p>
      </div>
    )
  }

  return (
    <div>
      <div className="notes-header">
        <h1 className="notes-title">My Notes</h1>
        <button
          onClick={() => setIsCreating(true)}
          className="btn btn-primary"
        >
          + New Note
        </button>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          {success}
        </div>
      )}

      {/* Create Note Form */}
      {isCreating && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2 className="modal-title">Create New Note</h2>
              <button
                className="modal-close"
                onClick={() => setIsCreating(false)}
              >
                ×
              </button>
            </div>
            <NoteForm
              onSubmit={handleCreateNote}
              onCancel={() => setIsCreating(false)}
              isLoading={isCreating}
            />
          </div>
        </div>
      )}

      {/* Notes Grid */}
      {notes.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">📝</div>
          <h3>No notes yet</h3>
          <p>Create your first note to get started!</p>
        </div>
      ) : (
        <div className="notes-grid">
          {notes.map(note => (
            <NoteItem
              key={note.id}
              note={note}
              onEdit={handleEditNote}
              onDelete={handleDeleteNote}
              isEditing={editingNote?.id === note.id}
              onSave={handleUpdateNote}
              onCancel={handleCancelEdit}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default Notes
