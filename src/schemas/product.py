from decimal import Decimal
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from src.schemas.category import CategoryRead


class ProductCategory(str, Enum):
    PHONES = "phones"
    LAPTOPS = "laptops"
    TABLETS = "tablets"
    TV = "tv"


class ProductBase(BaseModel):
    name: str
    description: str
    price: Decimal
    quantity: int
    image_url: Optional[str] = None
    product_category: ProductCategory


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    quantity: Optional[int] = None
    image_url: Optional[str] = None
    product_category: Optional[ProductCategory] = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    categories: List[CategoryRead] = []

    class Config:
        orm_mode = True
