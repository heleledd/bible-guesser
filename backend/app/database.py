from sqlmodel import Session, SQLModel, create_engine
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # path to backend/app/
DB_PATH = os.path.join(BASE_DIR, "database.db")

SQLITE_URL = f"sqlite:///{DB_PATH}"

connect_args = {"check_same_thread": False}
engine = create_engine(
    SQLITE_URL, 
    echo=True, 
    connect_args=connect_args
    )

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session