from sqlmodel import Session, select
from sqlalchemy import func
from pathlib import Path
import json
from dotenv import load_dotenv
from os import getenv
from database import engine
from models.verse_model import Verse

load_dotenv()
bible_json_path = Path(__file__).parent / getenv("BIBLE_JSON")

async def populate_verses():
    # Check if database is already populated
    with Session(engine) as session:
        verse_count = session.exec(select(func.count(Verse.id))).one()
        if verse_count > 0:
            print(f"Database already contains {verse_count} verses")
            return

        print("Populating database with verses...")
        # Load verses from your JSON file
        with open(bible_json_path, "r", encoding="utf-8") as f:
            verses = json.load(f)
        
        # Insert verses in chunks
        chunk_size = 500
        for i in range(0, len(verses), chunk_size):
            chunk = verses[i:i + chunk_size]
            db_verses = [
                Verse(
                    book_name=verse["book_name"],
                    book=verse["book"],
                    chapter=verse["chapter"],
                    verse=verse["verse"],
                    text=verse["text"]
                ) for verse in chunk
            ]
            session.add_all(db_verses)
            session.commit()
            print(f"Inserted verses {i} to {i + len(chunk)}")
