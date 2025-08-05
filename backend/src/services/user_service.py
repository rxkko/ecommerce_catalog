from fastapi import HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone
import logging

from src.core.security import get_password_hash, verify_password
from src.services.token_service import TokenService
from src.schemas.user import UserCreate, UserUpdate
from src.models.user import User
from src.core.config import settings

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class UserService:

    def __init__(self, user_repository, token_service: TokenService):
        self.user_repo = user_repository
        self.token_service = token_service

    async def authenticate_user(self, email: str, password: str) -> User:
        try:
            user = await self.user_repo.get_user_by_email(email)
            if not user or not verify_password(password, user.hashed_password):
                logger.warning(f"Неудачная попытка входа для email: {email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный email или пароль",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
            if not user.is_active:
                logger.warning(f"Попытка входа неактивного пользователя: {email}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Пользователь неактивен"
                )
                
            return user
            
        except Exception as e:
            logger.error(f"Ошибка аутентификации: {str(e)}")
            raise

    async def login(self, email: str, password: str, response: Response) -> dict:
        try:
            user = await self.authenticate_user(email, password)
            token_pair = self.token_service.create_token_pair(str(user.id))
            
            self.token_service.set_auth_cookies(response, token_pair)
            
            return {
                "message": "Успешный вход",
                "user_id": str(user.id),
                "email": user.email,
                "is_admin": user.is_admin
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Ошибка входа: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при входе в систему"
            )

    async def create_user(self, user_data: UserCreate) -> User:
        try:
            existing_user = await self.user_repo.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Пользователь с таким email уже существует"
                )
            
            existing_username = await self.user_repo.get_user_by_username(user_data.username)
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Пользователь с таким username уже существует"
                )    
            
            user_dict = user_data.model_dump()
            user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
            user_dict["created_at"] = datetime.now(timezone.utc).replace(tzinfo=None)
            return await self.user_repo.create_user(user_dict)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Ошибка создания пользователя: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при создании пользователя"
            )

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        try:
            update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if 'password' in update_data:
                update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
                
            return await self.user_repo.update_user(user_id, update_data)
            
        except Exception as e:
            logger.error(f"Ошибка обновления пользователя {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при обновлении пользователя"
            )

    async def delete_user(self, user_id: int) -> None:
        try:
            await self.user_repo.delete_user(user_id)
        except Exception as e:
            logger.error(f"Ошибка удаления пользователя {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при удалении пользователя"
            )

    async def logout(self, response: Response) -> dict:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"message": "Успешный выход"}
    
    async def get_users(self) -> list[User]:
        try:
            return await self.user_repo.get_users()
        except Exception as e:
            logger.error(f"Ошибка получения списка пользователей: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении списка пользователей"
            )

    # def _set_auth_cookies(self, response: Response, token_pair: TokenPair) -> None:
    #     cookie_params = {
    #         "httponly": True,
    #         "secure": True,
    #         "samesite": "lax",
    #         "path": "/",
    #     }
        
    #     response.set_cookie(
    #         key="access_token",
    #         value=token_pair.access_token,
    #         max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    #         **cookie_params
    #     )
        
    #     response.set_cookie(
    #         key="refresh_token",
    #         value=token_pair.refresh_token,
    #         max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    #         **cookie_params
    #     )

    async def deactivate_user():
        pass