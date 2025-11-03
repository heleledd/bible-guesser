import { useState, useEffect } from 'react'
import axios from 'axios'

function Game() {
  const [verse, setVerse] = useState('')
  const [guess, setGuess] = useState({ book: '', chapter: '', verse: '' })
  const [score, setScore] = useState(0)

  useEffect(() => {
    fetchNewVerse()
  }, [])

  const fetchNewVerse = async () => {
    // TODO: Implement API call to get random verse
    // setVerse(data.verse)
    // const response = await axios.get('/api/random-verse')
    // setVerse(response.data.verse)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // TODO: Implement guess verification
    // if (isCorrect) setScore(score + 1)
    // 
    fetchNewVerse()
  }

  return (
    <div className="game-container">
      <h2>Guess the Bible Verse</h2>
      <div className="verse-display">
        <p>{verse}</p>
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Book"
          value={guess.book}
          onChange={(e) => setGuess({ ...guess, book: e.target.value })}
        />
        <input
          type="number"
          placeholder="Chapter"
          value={guess.chapter}
          onChange={(e) => setGuess({ ...guess, chapter: e.target.value })}
        />
        <input
          type="number"
          placeholder="Verse"
          value={guess.verse}
          onChange={(e) => setGuess({ ...guess, verse: e.target.value })}
        />
        <button type="submit">Submit Guess</button>
      </form>
      <div className="score">
        Score: {score}
      </div>
    </div>
  )
}

export default Game