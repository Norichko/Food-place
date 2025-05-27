from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: str
    locationNow: Optional[str]
    favorites: Optional[List[str]] = []

class UserResponse(BaseModel):
    user: UserOut
    token: str
