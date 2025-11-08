from sqlmodel import SQLModel
from typing import Optional

"""Model for JWT token payload data"""
class TokenData(SQLModel):
    username: Optional[str] = None
    exp: Optional[int] = None  # Expiration timestamp
