from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel
from src.schemas.category import CategoryRead

class ProductBase(BaseModel):
    """Базовая модель товара"""
    name: str
    description: str
    price: Decimal
    quantity: int
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    """Модель для обновления товара"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    quantity: Optional[int] = None
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    """Модель для создания товара"""
    pass


class ProductRead(ProductBase):
    id: int
    categories: List[CategoryRead] = []

    class Config:
        orm_mode = True
