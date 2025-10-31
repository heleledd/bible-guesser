from sqlmodel import Field, Session, SQLModel, create_engine, select
from models.verse_model import Verse  
from models.user_model import User

SQLITE_FILE_NAME = "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

connect_args = {"check_same_thread": False}
engine = create_engine(
    SQLITE_URL, 
    echo=True, 
    connect_args=connect_args
    )

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
