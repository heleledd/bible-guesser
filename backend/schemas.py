from pydantic import BaseModel

# Shared fields
class UserBase(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None

# For creating a user (includes password)
class UserCreate(UserBase):
    password: str

# For returning a user (to client)
class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

# For internal use (e.g., includes hashed_password)
class UserInDB(UserBase):
    hashed_password: str