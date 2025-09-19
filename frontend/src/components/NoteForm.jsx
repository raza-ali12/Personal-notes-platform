import { useState } from 'react'

const NoteForm = ({ note, onSubmit, onCancel, isLoading }) => {
  const [formData, setFormData] = useState({
    title: note?.title || '',
    content: note?.content || ''
  })
  const [errors, setErrors] = useState({})

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (validateForm()) {
      onSubmit(formData)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="title" className="form-label">
          Title *
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className="form-input"
          placeholder="Enter note title"
          disabled={isLoading}
        />
        {errors.title && (
          <div className="alert alert-error">
            {errors.title}
          </div>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="content" className="form-label">
          Content
        </label>
        <textarea
          id="content"
          name="content"
          value={formData.content}
          onChange={handleChange}
          className="form-input form-textarea"
          placeholder="Enter note content"
          disabled={isLoading}
        />
      </div>

      <div style={{ display: 'flex', gap: '1rem' }}>
        <button
          type="submit"
          className="form-button"
          disabled={isLoading}
        >
          {isLoading ? 'Saving...' : (note ? 'Update Note' : 'Create Note')}
        </button>
        
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="btn btn-secondary"
            disabled={isLoading}
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  )
}

export default NoteForm
