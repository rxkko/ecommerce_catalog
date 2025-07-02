from fastapi import HTTPException, Response, status
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional
from src.schemas.token import TokenData, TokenPair
from src.core.config import settings


class TokenService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 30
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = timedelta(minutes=access_token_expire_minutes)
        self.refresh_token_expire = timedelta(days=refresh_token_expire_days)

    def _create_token(
        self,
        data: TokenData,
        expires_delta: timedelta
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_access_token(self, user_id: str) -> str:
        return self._create_token(
            {"sub": user_id},
            self.access_token_expire
        )

    def create_refresh_token(self, user_id: str) -> str:
        return self._create_token(
            {"sub": user_id},
            self.refresh_token_expire
        )

    def create_token_pair(self, user_id: str) -> TokenPair:
        return TokenPair(
            access_token=self.create_access_token(user_id),
            refresh_token=self.create_refresh_token(user_id)
        )

    def verify_token(self, token: str) -> Optional[TokenData]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return TokenData(**payload)
        except JWTError as e:
            raise ValueError("Invalid token") from e
        
    async def refresh_tokens(self, refresh_token: str, response: Response) -> dict:
        try:
            payload = self.token_service.verify_token(refresh_token)
            user_id = payload.get("sub")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный refresh token"
                )
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный тип токена"
                )
            token_pair = self.token_service.create_token_pair(user_id)
            response.set_cookie(key="access_token", value=token_pair.access_token, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60)
            response.set_cookie(key="refresh_token", value=token_pair.refresh_token, httponly=True, max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS*24*3600)
            
            return {
                "message": "Токены обновлены",
                "user_id": user_id
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный или истекший refresh token"
            )
    