from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel


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

    class Config:
        from_attributes = True   


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
    
    class Config:
        from_attributes = True

class AddToCart(BaseModel):
    user_id: int
    product_id: int
    quantity: Optional[str] = 1

    class Config:
        from_attributes = True