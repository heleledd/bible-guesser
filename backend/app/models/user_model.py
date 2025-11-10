from sqlmodel import Field, SQLModel

"""Base"""
class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    disabled: bool = Field(default=False, index=True)
    score: int = Field(default=0, index=True, description="Leaderboard score")

"""Database Model"""
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, unique=True)
    hashed_password: str

"""Create Model (for POST /users)"""
class UserCreate(UserBase):
    password: str  # Only used for account creation, not stored directly in the same model

"""Read Model (for API responses)"""
class UserPublic(UserBase):
    id: int
    
"""Update Model (optional, for returning the user's score)"""
class UserUpdate(SQLModel):
    username: str | None = None
    score: int | None = None
    
"""Score Update Model (for PATCH /users/score/update)"""
class UserScoreUpdate(SQLModel):
    score_change: int
