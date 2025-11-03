import { useState, useEffect } from 'react'
import axios from 'axios'
import { verses } from '../../services/api'

function Game() {
  const [verse, setVerse] = useState({book_name:'', book:0, chapter:0, verse:0, text:''})
  const [guess, setGuess] = useState({ book: '', chapter: '', verse: '' })
  const [score, setScore] = useState(0)

  useEffect(() => {
    fetchNewVerse()
  }, [])

  const fetchNewVerse = async () => {
    try {
      setError('')
      const data = await verses.getRandomVerse()
      setVerse(data)
    } catch (error) {
      setError('Failed to load verse. Please try again.')
      console.error('Error fetching random verse:', error)
    }
  }
  
  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')
    
    // Verify the guess
    if (
      guess.book.toLowerCase() === verse.book_name.toLowerCase() &&
      Number(guess.chapter) === verse.chapter &&
      Number(guess.verse) === verse.verse
    ) {
      setScore(score + 1)
    }

  return (
    <div className="game-container">
      <h2>Guess the Bible Verse</h2>
      <div className="verse-display">
        <p>{verse.text}</p>
      </div>
      <form onSubmit={refreshNewVerse}>
        <button type="submit">Refresh Verse</button>
      </form>
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
}

export default Game