from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.constants.enums import UserRole

class UserRegister(BaseModel):
    nama: str
    email: str
    password: str
    nim_nip: Optional[str] = None
    no_hp: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    nama: str
    email: str
    role: UserRole
    nim_nip: Optional[str] = None
    no_hp: Optional[str] = None
    foto: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True