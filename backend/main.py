from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, Integer, String, Text, Boolean, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Session
from database import SessionLocal, engine, Base
from typing import Annotated
from pydantic import BaseModel

import models, schemas

# Create database tables
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

###### models #####


    
class UserInDB(User):
    hashed_password = Column(String)

def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user



######## endpoints for user management below ########

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.get("/testing")
async def get_users(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

###### endpoints for verses below ######

@app.get("/verses/")
def get_verses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Verse).offset(skip).limit(limit).all()

@app.get("/verses/{book}")
def get_verses_by_book(book: str, db: Session = Depends(get_db)):
    return db.query(Verse).filter(Verse.book == book).all()

@app.get("/verses/{book}/{chapter}")
def get_verses_by_chapter(book: str, chapter: int, db: Session = Depends(get_db)):
    return db.query(Verse).filter(
        Verse.book == book,
        Verse.chapter == chapter
    ).all()

@app.get("/verses/{book}/{chapter}/{verse}")
def get_verse(book: str, chapter: int, verse: int, db: Session = Depends(get_db)):
    return db.query(Verse).filter(
        Verse.book == book,
        Verse.chapter == chapter,
        Verse.verse == verse
    ).first()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + SQLite!"}
