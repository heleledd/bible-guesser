from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from contextlib import asynccontextmanager
from sqlmodel import Session, select

# local imports
from database import create_db_and_tables, engine
from models.user_model import User, UserCreate, UserPublic, UserUpdate
from models.verse_model import Verse, VersePublic
from populate_verse_table.populate_verses import populate_verses


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    print("Starting up...")
    create_db_and_tables()
    await populate_verses()
    yield
    # Shutdown: add cleanup here if needed
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)


###### endpoints for verses below ######

@app.get("/verses/", response_model=list[VersePublic])
def read_verses():
    with Session(engine) as session:
        verses = session.exec(select(Verse)).all()
        return verses

@app.get("/verses/{book}", response_model=list[VersePublic])
def get_verses_by_book(book: str):
    with Session(engine) as session:
        verses = session.exec(select(Verse).where(Verse.book_name == book)).all()
        if not verses:
            raise HTTPException(status_code=404, detail="Book not found")
        return verses

@app.get("/verses/{book}/{chapter}", response_model=list[VersePublic])
def get_verses_by_chapter(book: str, chapter: int):
    with Session(engine) as session:
        verses = session.exec(select(Verse).where(
            Verse.book_name == book,
            Verse.chapter == chapter
        )).all()
        if not verses:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return verses

@app.get("/verses/{book}/{chapter}/{verse}", response_model=VersePublic)
def get_verse_by_reference(book: str, chapter: int, verse: int):
    with Session(engine) as session:
        verse = session.exec(select(Verse).where(
            Verse.book_name == book,
            Verse.chapter == chapter,
            Verse.verse == verse
        )).first()
        if not verse:
            raise HTTPException(status_code=404, detail="Verse not found")
        return verse

@app.get("/")
def read_root():
    return {"message": "Hello Bible Guesser!"}
