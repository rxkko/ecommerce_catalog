from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel
from src.schemas.category import CategoryRead

class ProductBase(BaseModel):
    name: str
    description: str
    price: Decimal
    quantity: int
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    category_ids: List[int]  # Список id категорий, к которым относится товар


class ProductRead(ProductBase):
    id: int
    categories: List[CategoryRead] = []

    class Config:
        orm_mode = True
