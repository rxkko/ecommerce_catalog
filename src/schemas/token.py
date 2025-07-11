from pydantic import BaseModel
from typing import TypedDict
from datetime import datetime


class TokenData(BaseModel):
    sub: str
    type: str
    exp: datetime

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str