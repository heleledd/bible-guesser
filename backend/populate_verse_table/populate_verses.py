from sqlmodel import Session, select
from sqlalchemy import func
from pathlib import Path
import json
from database import engine
from models.verse_model import Verse


BIBLE_JSON = Path(__file__).parent / "json_bibles/kjv_bible.json"

async def populate_verses():
    # Check if database is already populated
    with Session(engine) as session:
        verse_count = session.exec(select(func.count(Verse.id))).one()
        if verse_count > 0:
            print(f"Database already contains {verse_count} verses")
            return

        print("Populating database with verses...")
        # Load verses from your JSON file
        with open(BIBLE_JSON, "r", encoding="utf-8") as f:
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
