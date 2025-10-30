from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/verses/")
def get_verses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Verse).offset(skip).limit(limit).all()

@app.get("/verses/{book}")
def get_verses_by_book(book: str, db: Session = Depends(get_db)):
    return db.query(models.Verse).filter(models.Verse.book == book).all()

@app.get("/verses/{book}/{chapter}")
def get_verses_by_chapter(book: str, chapter: int, db: Session = Depends(get_db)):
    return db.query(models.Verse).filter(
        models.Verse.book == book,
        models.Verse.chapter == chapter
    ).all()

@app.get("/verses/{book}/{chapter}/{verse}")
def get_verse(book: str, chapter: int, verse: int, db: Session = Depends(get_db)):
    return db.query(models.Verse).filter(
        models.Verse.book == book,
        models.Verse.chapter == chapter,
        models.Verse.verse == verse
    ).first()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + SQLite!"}
