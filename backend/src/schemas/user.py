from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr = Field(..., example="user@example.com")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)


class UserUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    is_admin: bool | None = None


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str