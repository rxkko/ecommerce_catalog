from pydantic import BaseModel
from src.schemas.product import ProductBase
from typing import List


class CartResponse(BaseModel):
    products: List[ProductBase]
    total_price: float

    class Config:
        from_attributes = True