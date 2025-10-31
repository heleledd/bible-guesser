from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from typing import Annotated
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from os import getenv
import jwt
import uvicorn
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash


# local imports
from database import create_db_and_tables, get_session
from models.user_model import User, UserCreate, UserPublic, UserUpdate
from models.verse_model import Verse, VersePublic
from models.token_model import Token, TokenData
from populate_verse_table.populate_verses import populate_verses

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

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

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(session, username: str):
    user = session.exec(select(User).where(User.username == username)).first()
    if user:
        return user
    else:
        return None


def authenticate_user(session, username: str, password: str):
    user = get_user(session=session, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(session=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

"""Any route depending on this requires a valid JWT bearer token"""
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

"""Login endpoint to get JWT token"""
@app.post("/users/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_session)
    ) -> Token:
    user = authenticate_user(session=session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


"""Sign In endpoint"""
@app.post("/users/signin", response_model=UserPublic)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    # Check if username already exists
    db_user = session.exec(
        select(User).where(User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        disabled=False,
        score=0
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

###### endpoints for users below ######

@app.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ):
    return [{"item_id": "Foo", "owner": current_user.username}]


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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)