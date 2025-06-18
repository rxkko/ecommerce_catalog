from src.core.security import get_password_hash, verify_password
from datetime import datetime, timedelta, timezone
from jose import jwt


class TokenService:
    def __init__(self, expires_delta: timedelta | None = None):
        self.expires_delta = expires_delta

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        if self.expires_delta:
            expire = datetime.now(timezone.utc) + self.expires_delta
        else:
            expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, "your_secret_key", algorithm="HS256")
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        if self.expires_delta:
            expire = datetime.now(timezone.utc) + self.expires_delta
        else:
            expire = datetime.datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, "your_secret_key", algorithm="HS256")
        return encoded_jwt
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
            return payload
        except jwt.JWTError:
            return None
        except Exception as e:
            print(f"Ошибка при проверке токена: {e}")
            return None

    