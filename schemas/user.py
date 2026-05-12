from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.constants.enums import UserRole

class UserBase(BaseModel):
    nama: str
    email: str
    role: UserRole
    nim_nip: Optional[str] = None
    no_hp: Optional[str] = None
    foto: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):

    id: int
    created_at: datetime

    class Config:
        from_attributes = True