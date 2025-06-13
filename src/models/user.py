from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())