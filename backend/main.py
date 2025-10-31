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

# @app.get("/verses/")
# def get_verses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return db.exec(select(Verse).offset(skip).limit(limit)).all()

# @app.get("/verses/{book}")
# def get_verses_by_book(book: str, db: Session = Depends(get_db)):
#     return db.query(Verse).filter(Verse.book == book).all()

# @app.get("/verses/{book}/{chapter}")
# def get_verses_by_chapter(book: str, chapter: int, db: Session = Depends(get_db)):
#     return db.query(Verse).filter(
#         Verse.book == book,
#         Verse.chapter == chapter
#     ).all()

# @app.get("/verses/{book}/{chapter}/{verse}")
# def get_verse(book: str, chapter: int, verse: int, db: Session = Depends(get_db)):
#     return db.query(Verse).filter(
#         Verse.book == book,
#         Verse.chapter == chapter,
#         Verse.verse == verse
#     ).first()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + SQLite!"}
