import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './hooks/useAuth.jsx'
import NavBar from './components/NavBar'
import Login from './pages/Login'
import Register from './pages/Register'
import Notes from './pages/Notes'

function AppContent() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <Router>
      <div className="app">
        <NavBar />
        <main className="main-content">
          <Routes>
            <Route 
              path="/login" 
              element={user ? <Navigate to="/notes" replace /> : <Login />} 
            />
            <Route 
              path="/register" 
              element={user ? <Navigate to="/notes" replace /> : <Register />} 
            />
            <Route 
              path="/notes" 
              element={user ? <Notes /> : <Navigate to="/login" replace />} 
            />
            <Route 
              path="/" 
              element={<Navigate to={user ? "/notes" : "/login"} replace />} 
            />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
