import { Link, useNavigate } from 'react-router-dom'
import { auth } from '../../services/api'
import bookImage from '../../images/book.svg'
import "../../styles/Navbar.css"

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
      <div className="nav-left">
        <img src={bookImage} alt="Bible Guesser" className="headerImage" />
        <div className="nav-brand">
          <Link to="/">Bible Guesser</Link>
        </div>
      </div>

      <div className="nav-links">
        {isAuthenticated ? (
          <>
            <Link to="/game" className="outline-btn">Game</Link>
            <Link to="/leaderboard" className="outline-btn">Leaderboard</Link>
            <button onClick={handleLogout} className="outline-btn">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="outline-btn">Login</Link>
            <Link to="/signup" className="outline-btn">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  )
}

export default Navbar