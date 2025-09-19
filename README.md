# Notes Platform

A full-stack notes application built with Flask (Python) backend and React frontend, featuring user authentication and CRUD operations for personal notes.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Or Python 3.11+ and Node.js 18+ for local development

### Option 1: Docker (Recommended)
```bash
# Clone and navigate to the project
git clone <repository-url>
cd "Notes (Flask + React)"

# Start both backend and frontend
docker-compose up --build

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:5000
```

### Option 2: Local Development

#### Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env.example .env
# Edit .env with your configuration

# Initialize database
python create_db.py

# Run the backend
python app.py
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp env.example .env
# Edit .env with your API URL

# Start development server
npm run dev
```

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with Flask-JWT-Extended
- **Validation**: Marshmallow schemas
- **CORS**: Flask-CORS for frontend integration
- **Testing**: pytest

### Frontend (React)
- **Framework**: React 18 with Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios with interceptors
- **State Management**: React Context for auth
- **Testing**: Vitest + Testing Library

## 📡 API Reference

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (201)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2023-12-01T10:00:00Z"
}
```

#### Login User
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200)**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2023-12-01T10:00:00Z"
  }
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <jwt_token>
```

**Response (200)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2023-12-01T10:00:00Z"
}
```

### Notes Endpoints

#### Get All Notes
```http
GET /api/notes
Authorization: Bearer <jwt_token>
```

**Response (200)**:
```json
[
  {
    "id": 1,
    "title": "My First Note",
    "content": "This is the content of my note",
    "user_id": 1,
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T10:00:00Z"
  }
]
```

#### Create Note
```http
POST /api/notes
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "New Note",
  "content": "Note content here"
}
```

#### Update Note
```http
PUT /api/notes/1
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

#### Delete Note
```http
DELETE /api/notes/1
Authorization: Bearer <jwt_token>
```

**Response (204)**: No content

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Security Features

- Password hashing with Werkzeug
- JWT token authentication (1-day expiry)
- User isolation (users can only access their own notes)
- CORS protection
- Input validation and sanitization
- SQL injection protection via ORM


## 🐳 Docker Details

### Backend Container
- Base: `python:3.11-slim`
- Port: 5000
- Environment variables from `.env`
- Volume mount for development

### Frontend Container
- Base: `node:20-alpine`
- Port: 5173
- Production build served with `serve`
- Volume mount for development

## 🚀 Deployment

### Production Considerations
1. Change default secret keys in environment variables
2. Use a production database (PostgreSQL recommended)
3. Set up proper CORS origins
4. Use environment-specific configurations
5. Set up SSL/TLS certificates
6. Configure proper logging and monitoring

### Environment Variables

#### Backend (.env)
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///app.db
CORS_ORIGINS=http://localhost:5173
FLASK_ENV=development
```

#### Frontend (.env)
```
VITE_API_URL=http://localhost:5000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

