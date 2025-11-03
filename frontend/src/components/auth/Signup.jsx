import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Signup({ setIsAuthenticated }) {
  const [userData, setUserData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    // TODO: Implement API call to backend
    setIsAuthenticated(true)
    navigate('/game')
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