import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './auth/Login'
import Signup from './auth/Signup'
import Game from './game/Game'
import Leaderboard from './game/Leaderboard'
import Navbar from './common/Navbar'

function Main() {
  const [isAuthenticated, setIsAuthenticated] = useState(true)
  const [user, setUser] = useState({ username: '' })

  return (
    <Router>
      <div className="app-container">
        <Navbar isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
        
        <div style={{ padding: '4px', fontSize: '12px', color: '#666' }}>
          {isAuthenticated ? (
            <>Logged in as <strong>{user.username}</strong></>
          ) : (
            'Not logged in'
          )}
        </div>

        <Routes>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} setUser={setUser} />} />
          <Route path="/signup" element={<Signup setIsAuthenticated={setIsAuthenticated} setUser={setUser} />} />
          <Route path="/game" element={<Game isAuthenticated={isAuthenticated} />} />
          <Route 
            path="/leaderboard" 
            element={isAuthenticated ? <Leaderboard /> : <Navigate to="/login" />} 
          />
          <Route path="/" element={<Navigate to="/game" />} />
        </Routes>
      </div>
    </Router>
  )
}

export default Main