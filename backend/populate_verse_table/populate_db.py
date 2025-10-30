# populate_db.py
import json
from pathlib import Path
from database import SessionLocal, engine
import models
from sqlalchemy.orm import Session

# make sure tables exist
models.Base.metadata.create_all(bind=engine)

BIBLE_JSON = Path(__file__).parent / "bible.json"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def chunked(iterable, size):
    it = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(size):
                chunk.append(next(it))
        except StopIteration:
            if chunk:
                yield chunk
            break
        yield chunk

def main():
    data = load_json(BIBLE_JSON)  # expect list of dicts with keys: book, chapter, verse, text
    db: Session = SessionLocal()
    try:
        # Prepare objects
        objs = [
            models.Verse(
                book_name=v["book_name"],
                book=v["book"], 
                chapter=int(v["chapter"]), 
                verse=int(v["verse"]), 
                text=v["text"]
            ) for v in data]

        # Insert in chunks to avoid huge memory/transaction problems
        CHUNK = 500  # tune this for your machine
        for i, chunk in enumerate(chunked(objs, CHUNK), start=1):
            db.bulk_save_objects(chunk)
            db.commit()
            print(f"Committed chunk {i}, {len(chunk)} verses")
        print("Done.")
    finally:
        db.close()

if __name__ == "__main__":
    main()