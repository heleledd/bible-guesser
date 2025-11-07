import { useState, useEffect } from 'react'
import { verses } from '../../services/api'

function Game() {
  const [verse, setVerse] = useState({book_name:'', book:0, chapter:0, verse:0, text:''})
  const [guess, setGuess] = useState({ book: '', chapter: '', verse: '' })
  const [score, setScore] = useState(0)
  const [error, setError] = useState('Oh no! Something went wrong.')
  const [loading, setLoading] = useState(false)
  const [scoreMessage, setScoreMessage] = useState('Let\'s start guessing!')

  useEffect(() => {
    fetchNewVerse()
  }, [])

  const fetchNewVerse = async () => {
    setLoading(true)
    setError('')

    try {  
      const data = await verses.getRandomVerse()
      setVerse(data)
    } catch (error) {
      setError('Failed to load verse. Please try again.')
      console.error('Error fetching random verse:', error)
    } finally {
      setLoading(false)
    }
  }
  
  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    
    let newPoints = 0;

    const guessedBook = guess.book.trim().toLowerCase();
    const actualBook = verse.book_name.trim().toLowerCase();

    // Book correct
    if (guessedBook === actualBook) {
      newPoints += 50;

      // Chapter correct
      if (Number(guess.chapter) === verse.chapter) {
        newPoints += 30;

        // Verse close or exact (within ±2)
        const verseDiff = Math.abs(Number(guess.verse) - verse.verse);
        if (verseDiff === 0) {
          newPoints += 20; // perfect verse
        } else if (verseDiff <= 2) {
          newPoints += 10; // close enough
        }
      }
    }

    if (newPoints === 0) {
      setScoreMessage('Incorrect! Keep trying! The correct answer was ' + `${verse.book_name} ${verse.chapter}:${verse.verse}.`);
    } else {
      setScore((prev) => prev + newPoints);
      setScoreMessage(`Nice! You earned ${newPoints} points. The correct answer was ` + `${verse.book_name} ${verse.chapter}:${verse.verse}.`);

      // update user score in backend!!
      
    }


    // Load next verse
    fetchNewVerse();
  };

  return (
    <div className="game-container">
      <h2>Guess the Bible Verse</h2>
       <div className="verse-display">
        {loading ? (
          <p>Loading verse...</p>
        ) : (
          <p>{verse.text || 'No verse loaded'}</p>
        )}
      </div>
      <button onClick={fetchNewVerse}>Refresh Verse</button>
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
        {scoreMessage && <div className="score-message">{scoreMessage}</div>}
        Score: {score}
      </div> 
    </div>
  )
}


export default Game;