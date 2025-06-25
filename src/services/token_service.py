from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional
from src.schemas.token import TokenData, TokenPair


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

    