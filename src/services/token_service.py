from fastapi import HTTPException, Response, status
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional
import logging
from src.schemas.token import TokenData, TokenPair
from src.core.config import settings

logger = logging.getLogger(__name__)

class TokenService:

    def __init__(
        self,
        secret_key: str = settings.SECRET_KEY,
        algorithm: str = settings.ALGORITHM,
        access_token_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days: int = settings.REFRESH_TOKEN_EXPIRE_DAYS
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = timedelta(minutes=access_token_expire_minutes)
        self.refresh_token_expire = timedelta(days=refresh_token_expire_days)

    def _create_token(
        self,
        data: dict,
        expires_delta: timedelta,
        token_type: str
    ) -> str:
        try:
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + expires_delta
            to_encode.update({
                "exp": expire,
                "type": token_type,
                "iss": settings.JWT_ISSUER
            })
            logger.debug(f"Создание токена типа {token_type}, срок: {expires_delta}")
            return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            logger.error(f"Ошибка создания токена: {str(e)}")
            raise ValueError("Не удалось создать токен") from e

    def create_access_token(self, user_id: str) -> str:
        return self._create_token(
            {"sub": user_id},
            self.access_token_expire,
            "access"
        )

    def create_refresh_token(self, user_id: str) -> str:
        return self._create_token(
            {"sub": user_id},
            self.refresh_token_expire,
            "refresh"
        )

    def create_token_pair(self, user_id: str) -> TokenPair:
        return TokenPair(
            access_token=self.create_access_token(user_id),
            refresh_token=self.create_refresh_token(user_id)
        )

    def verify_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={
                    "require_iss": True,
                    "verify_iss": True,
                    "verify_exp": True
                },
                issuer=settings.JWT_ISSUER
            )
            return TokenData(**payload)
        except JWTError as e:
            logger.warning(f"Невалидный токен: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный или истекший токен",
                headers={"WWW-Authenticate": "Bearer"}
            )

    async def refresh_tokens(
        self, 
        refresh_token: str, 
        response: Response
    ) -> dict:
        try:
            token_data = self.verify_token(refresh_token)
            
            if token_data.type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный тип токена",
                    headers={"WWW-Authenticate": "Bearer"}
                )
                
            if not token_data.sub:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный формат токена",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            token_pair = self.create_token_pair(token_data.sub)
            
            self.set_auth_cookies(response, token_pair)
            print ("Токены обновленны")
            return {
                "message": "Токены успешно обновлены",
                "user_id": token_data.sub,
                "access_token": token_pair.access_token
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Ошибка обновления токенов: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не удалось обновить токены",
                headers={"WWW-Authenticate": "Bearer"}
            )

    def set_auth_cookies(self, response: Response, token_pair: TokenPair) -> None:
        cookie_params = {
            "httponly": True,
            "secure": True,
            "samesite": "lax",
            "path": "/",
        }
        
        response.set_cookie(
            key="access_token",
            value=token_pair.access_token,
            max_age=int(self.access_token_expire.total_seconds()),
            **cookie_params
        )
        
        response.set_cookie(
            key="refresh_token",
            value=token_pair.refresh_token,
            max_age=int(self.refresh_token_expire.total_seconds()),
            **cookie_params
        )