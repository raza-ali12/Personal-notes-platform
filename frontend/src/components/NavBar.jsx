import { useAuth } from '../hooks/useAuth.jsx'

const NavBar = () => {
  const { user, logout } = useAuth()

  return (
    <nav className="navbar">
      <a href="/" className="navbar-brand">
        📝 Notes App
      </a>
      
      <div className="navbar-nav">
        {user ? (
          <>
            <span className="navbar-user">
              Welcome, {user.email}
            </span>
            <button 
              onClick={logout}
              className="btn btn-secondary btn-sm"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <a href="/login" className="btn btn-primary btn-sm">
              Login
            </a>
            <a href="/register" className="btn btn-secondary btn-sm">
              Register
            </a>
          </>
        )}
      </div>
    </nav>
  )
}

export default NavBar
