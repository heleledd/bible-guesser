import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { auth } from '../../services/api'

function Login({ setIsAuthenticated, setUser }) {
  const [credentials, setCredentials] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    try {
      // Login and get token
      const data = await auth.login(credentials.username, credentials.password)
      
      // Store the token
      localStorage.setItem('token', data.access_token)
      
      // Verify token by fetching user data
      const user_response = await auth.getCurrentUser()

      setUser({ username: user_response.username })
      setIsAuthenticated(true)
      navigate('/game')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to login. Please check your credentials.')
    }
  }

  return (
    <div className="auth-container">
      <h2>Login</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={credentials.username}
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  )
}

export default Login
