from src.core.security import get_password_hash
from src.services.token_service import TokenService
from src.schemas.user import UserCreate, UserUpdate
from src.models.user import User
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, Annotated
from fastapi import Depends, Response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class UserService:
    def __init__(self, user_repository, token_service: TokenService):
        self.user_repo = user_repository
        self.token_service = token_service

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.user_repo.get_user_by_email(email)
        return user

    async def login(self, email: str, password: str, response: Response) -> dict:
        user = await self.authenticate_user(email, password)
        token_pair = self.token_service.create_token_pair(str(user.id))
        return {
            "message": "Успешный вход", 
            "user_id": user.id,
            "email": user.email
        }

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        payload = self.token_service.verify_token(token)
        user_id = payload.get("sub")
        return await self.user_repo.get_user_by_id(int(user_id))

    async def create_user(self, user_data: UserCreate) -> User:
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        return await self.user_repo.create_user(user_dict)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        update_data = user_data.model_dump(exclude_unset=True)
        if 'password' in update_data:
            update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
        return await self.user_repo.update_user(user_id, update_data)

    async def delete_user(self, user_id: int) -> dict:
        await self.user_repo.delete_user(user_id)
        return {"message": "Пользователь успешно удален"}

    async def logout(self, response: Response) -> dict:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"message": "Успешный выход"}