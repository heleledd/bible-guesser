import { useState, useEffect } from 'react'
import { leaderboard as leaderboardAPI } from '../../services/api'
import "../../styles/Leaderboard.css"

function Leaderboard({ setIsAuthenticated, setUser }) {
  const [leaders, setLeaders] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchLeaderboard()
  }, [])

  const fetchLeaderboard = async () => {
    setLoading(true)
    setError('')

    try {
      const data = await leaderboardAPI.getLeaderboard()

      // Ensure every player has a score value
      const normalized = data.map(player => ({
        username: player.username || 'Unknown',
        score: player.score ?? 0,
      }))

      setLeaders(normalized)
    } catch (err) {
      console.error('Error fetching leaderboard:', err)
      setError('Failed to load leaderboard. Please try again later.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="leaderboard-container">
      <h2>Leaderboard</h2>
      <p>Behold!! The top players are:</p>

      {loading && <p>Loading leaderboard...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <div className="leaderboard-list">
          {leaders.length === 0 ? (
            <p>No players found yet!</p>
          ) : (
            leaders.map((entry, index) => (
              <div key={index} className="leaderboard-entry">
                <span className="rank">#{index + 1}</span>
                <span className="username">{entry.username}</span>
                <span className="score">{entry.score}</span>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}

export default Leaderboard