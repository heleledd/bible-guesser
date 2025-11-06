import { useState, useEffect } from 'react'

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([])

  useEffect(() => {
    fetchLeaderboard()
  }, [])

  const fetchLeaderboard = async () => {
    // TODO: Implement API call to get leaderboard data
    // setLeaderboard(data)
  }

  return (
    <div className="leaderboard-container">
      <h2>Leaderboard</h2>
      <p>How do the points work??</p>
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