from datetime import datetime
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    name: str
    username: str
    password: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False


class UserUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    is_admin: bool | None = None


class UserRead(BaseModel):
    name: str
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True