import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './auth/Login'
import Signup from './auth/Signup'
import Game from './game/Game'
import Leaderboard from './game/Leaderboard'
import Navbar from './common/Navbar'

function Main() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  return (
    <Router>
      <div className="app-container">
        <Navbar isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
        <Routes>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/signup" element={<Signup setIsAuthenticated={setIsAuthenticated} />} />
          <Route 
            path="/game" 
            element={isAuthenticated ? <Game /> : <Navigate to="/login" />} 
          />
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