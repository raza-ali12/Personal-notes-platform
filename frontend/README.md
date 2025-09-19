# Notes Frontend

A React-based frontend for the Notes application built with Vite, React Router, and Axios.

## Features

- User authentication (login/register)
- JWT token management with localStorage
- Protected routes
- Notes CRUD operations
- Responsive design
- Real-time form validation
- Error handling and user feedback

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your API URL
```

3. Start development server:
```bash
npm run dev
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests with Vitest

## Project Structure

```
src/
├── api/
│   └── axios.js          # Axios instance with interceptors
├── components/
│   ├── NavBar.jsx        # Navigation component
│   ├── NoteForm.jsx      # Note creation/editing form
│   └── NoteItem.jsx      # Individual note display
├── hooks/
│   └── useAuth.js        # Authentication context and hooks
├── pages/
│   ├── Login.jsx         # Login page
│   ├── Register.jsx      # Registration page
│   └── Notes.jsx         # Notes list and management
├── __tests__/
│   └── Login.test.jsx    # Login component tests
├── App.jsx               # Main app component with routing
├── main.jsx              # App entry point
└── styles.css            # Global styles
```

## Authentication Flow

1. User registers/logs in
2. JWT token is stored in localStorage
3. Token is automatically attached to API requests
4. 401 responses trigger automatic logout and redirect to login
5. Protected routes check authentication status

## Docker

Build and run with Docker:
```bash
docker build -t notes-frontend .
docker run -p 5173:5173 notes-frontend
```
