from pydantic import BaseModel
from src.schemas.product import ProductBase
from typing import List


class CartResponse(BaseModel):
    products: List[ProductBase]

    class Config:
        from_attributes = True


class CartCount(BaseModel):
    count: int
    
    class Config:
        from_attributes = True