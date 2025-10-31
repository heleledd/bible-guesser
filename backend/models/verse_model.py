from sqlmodel import Field, SQLModel
 
###### base verse model
class VerseBase(SQLModel):
    book_name: str = Field(index=True)
    book: int = Field(index=True)
    chapter: int = Field(index=True)
    verse: int = Field(index=True)
    text: str = Field()

# database model
class Verse(VerseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# read model (for API responses)
class VersePublic(VerseBase):
    id: int