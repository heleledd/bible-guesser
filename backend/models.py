from sqlalchemy import Column, Integer, String
from database import Base

from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from database import Base


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

