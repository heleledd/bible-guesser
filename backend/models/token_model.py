from sqlmodel import SQLModel
from typing import Optional

"""Model for JWT token response"""
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

"""Model for JWT token payload data"""
class TokenData(SQLModel):
    username: Optional[str] = None
    exp: Optional[int] = None  # Expiration timestamp
