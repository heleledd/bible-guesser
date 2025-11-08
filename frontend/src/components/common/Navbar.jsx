import { Link, useNavigate } from 'react-router-dom'
import { auth } from '../../services/api'

function Navbar({ isAuthenticated, setIsAuthenticated }) {
  const navigate = useNavigate()

  const handleLogout = async () => {
    
    // clear cookies or tokens

    try {
      await auth.logout()
      setIsAuthenticated(false)
      setUser(null)
      navigate('/login') // redirect to login page
    } catch (err) {
      console.error("Failed to logout:", err)
    }
  }

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to="/">Bible Guesser</Link>
      </div>
      <div className="nav-links">
        {isAuthenticated ? (
          <>
            <Link to="/game">Game</Link>
            <Link to="/leaderboard">Leaderboard</Link>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  )
}

export default Navbar