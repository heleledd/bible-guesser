from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from typing import Annotated

# local imports
from database import create_db_and_tables, get_session
from models.user_model import User, UserCreate, UserPublic, UserUpdate
from models.verse_model import Verse, VersePublic
from populate_verse_table.populate_verses import populate_verses

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

### security tutorial ###

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


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


###### endpoints for users below ######



###### endpoints for verses below #######

# this might be a bit too chonky
@app.get("/verses/", response_model=list[VersePublic])
def read_verses(*, session: Session = Depends(get_session)):
        verses = session.exec(select(Verse)).all()
        return verses

@app.get("/verses/{book}", response_model=list[VersePublic])
def get_verses_by_book(*, session: Session = Depends(get_session),book: str):
    verses = session.exec(select(Verse).where(Verse.book_name == book)).all()
    if not verses:
        raise HTTPException(status_code=404, detail="Book not found")
    return verses

@app.get("/verses/{book}/{chapter}", response_model=list[VersePublic])
def get_verses_by_chapter(*, session: Session = Depends(get_session),book: str, chapter: int):
    verses = session.exec(select(Verse).where(
        Verse.book_name == book,
        Verse.chapter == chapter
    )).all()
    if not verses:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return verses

@app.get("/verses/{book}/{chapter}/{verse}", response_model=VersePublic)
def get_verse_by_reference(*, session: Session = Depends(get_session),book: str, chapter: int, verse: int):
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
    return {"message": "Hello there Bible Guesser!"}
