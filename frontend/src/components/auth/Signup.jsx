import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { auth } from '../../services/api'
import "../../styles/Auth.css"

function Signup({ setIsAuthenticated }) {
  const [userData, setUserData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const navigate = useNavigate()
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
        setError('')
        
        try {
          // Sign up
          const signup_data = await auth.signup(userData)
          
          // get token by logging in
          const login_data = await auth.login(userData.username, userData.password)
          
          // Verify token by fetching user data
          await auth.getCurrentUser()
          
          setIsAuthenticated(true)
          navigate('/game')
        } catch (err) {
          setError(err.response?.data?.detail || 'Failed to login. Please check your credentials.')
        }
  }

  return (
    <div className="auth-container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={userData.username}
          onChange={(e) => setUserData({ ...userData, username: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          value={userData.email}
          onChange={(e) => setUserData({ ...userData, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          value={userData.password}
          onChange={(e) => setUserData({ ...userData, password: e.target.value })}
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={userData.confirmPassword}
          onChange={(e) => setUserData({ ...userData, confirmPassword: e.target.value })}
        />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  )
}

export default Signup