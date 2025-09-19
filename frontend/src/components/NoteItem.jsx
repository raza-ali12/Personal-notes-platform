import { useState } from 'react'
import NoteForm from './NoteForm'

const NoteItem = ({ note, onEdit, onDelete, isEditing, onSave, onCancel }) => {
  const [isDeleting, setIsDeleting] = useState(false)

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      setIsDeleting(true)
      try {
        await onDelete(note.id)
      } finally {
        setIsDeleting(false)
      }
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (isEditing) {
    return (
      <div className="note-card">
        <NoteForm
          note={note}
          onSubmit={onSave}
          onCancel={onCancel}
        />
      </div>
    )
  }

  return (
    <div className="note-card">
      <div className="note-header">
        <h3 className="note-title">{note.title}</h3>
        <div className="note-actions">
          <button
            onClick={() => onEdit(note)}
            className="btn btn-primary btn-sm"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            className="btn btn-danger btn-sm"
            disabled={isDeleting}
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
      
      {note.content && (
        <div className="note-content">
          {note.content}
        </div>
      )}
      
      <div className="note-meta">
        Created: {formatDate(note.created_at)}
        {note.updated_at !== note.created_at && (
          <span> • Updated: {formatDate(note.updated_at)}</span>
        )}
      </div>
    </div>
  )
}

export default NoteItem
