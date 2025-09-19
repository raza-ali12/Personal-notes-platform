# Notes Backend

A Flask-based REST API for a notes application with user authentication and CRUD operations.

## Features

- User registration and authentication with JWT
- Secure password hashing
- Notes CRUD operations with user isolation
- SQLite database with SQLAlchemy ORM
- Input validation with Marshmallow
- CORS support for frontend integration
- Comprehensive test suite

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your configuration
```

3. Initialize the database:
```bash
python create_db.py
```

4. Run the application:
```bash
flask --app app.py run -p 5000 --debug
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info (requires JWT)

### Notes
- `GET /api/notes` - Get all user's notes (requires JWT)
- `POST /api/notes` - Create a new note (requires JWT)
- `GET /api/notes/:id` - Get a specific note (requires JWT)
- `PUT /api/notes/:id` - Update a note (requires JWT)
- `DELETE /api/notes/:id` - Delete a note (requires JWT)

## Testing

Run the test suite:
```bash
pytest
```

## Docker

Build and run with Docker:
```bash
docker build -t notes-backend .
docker run -p 5000:5000 --env-file .env notes-backend
```
