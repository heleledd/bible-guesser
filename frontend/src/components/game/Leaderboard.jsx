import { useState, useEffect } from 'react'
import { leaderboard } from '../../services/api'

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([])

  useEffect(() => {
    fetchLeaderboard()
  }, [])

  const fetchLeaderboard = async () => {
    const data = await leaderboard.getLeaderboard()
    setLeaderboard(data)

  }

  return (
    <div className="leaderboard-container">
      <h2>Leaderboard</h2>
      <p>Behold!! The top players are:</p>
      <div className="leaderboard-list">
        {leaderboard.map((entry, index) => (
          <div key={index} className="leaderboard-entry">
            <span className="rank">{index + 1}</span>
            <span className="username">{entry.username}</span>
            <span className="score">{entry.score}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Leaderboard