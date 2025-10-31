from sqlmodel import Field, Session, SQLModel, create_engine, select

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    score = Column(Integer, default=0)
    disabled = Column(Boolean, default=False)


class Verse(Base):
    __tablename__ = "verses"

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, index=True)  # e.g., "Genesis", "Exodus"
    book = Column(Integer, index=True)  # e.g., 1 for Genesis, 2 for Exodus
    chapter = Column(Integer, index=True)  # e.g., 1, 2, 3
    verse = Column(Integer, index=True)  # e.g., 1, 2, 3
    text = Column(Text)  # The actual verse text

    # Make book+chapter+verse combination unique
    __table_args__ = (
        UniqueConstraint('book', 'chapter', 'verse', name='unique_verse_location'),
    )

    def __repr__(self):
        return f"{self.book_name} {self.chapter}:{self.verse}"
    
    
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    pass


class HeroPublic(HeroBase):
    id: int