from fastapi import Depends
from typing import Annotated
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models.user import User
from sqlalchemy.future import select
from src.schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]):
        self.db = db

    async def get_users(self):
        users = await self.db.execute(select(User))
        return users.scalars().all()

    async def get_user_by_id(self, user_id: int):
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: EmailStr):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, user_data: dict):
        user = User(**user_data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_id: int, user_data: UserUpdate):
        user = await self.get_user_by_id(user_id)
        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int):
        user = await self.get_user_by_id(user_id)
        await self.db.delete(user)
        await self.db.commit()
        return {"message": "Пользователь успешно удален"}