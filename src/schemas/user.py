from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    password: str  # Исходный пароль для хэширования


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True