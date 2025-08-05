from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from pydantic import EmailStr
from fastapi import HTTPException, status

from src.dependencies.db_deps import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self) -> List[User]:
        try:
            result = await self.session.execute(select(User))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при получении пользователей: {str(e)}"
            )

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден"
                )
            return user
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при поиске пользователя: {str(e)}"
            )

    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(User).where(User.email.ilike(email)))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при поиске по email: {str(e)}"
            )
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при поиске по username: {str(e)}"
            )

    async def create_user(self, user_data: dict) -> User:
        try:
            user = User(**user_data)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при создании пользователя: {str(e)}"
            )

    async def update_user(self, user_id: int, user_data: dict) -> User:
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден"
                )

            for field, value in user_data.items():
                setattr(user, field, value)

            await self.session.commit()
            await self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при обновлении пользователя: {str(e)}"
            )

    async def delete_user(self, user_id: int) -> bool:
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден"
                )

            await self.session.delete(user)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при удалении пользователя: {str(e)}"
            )