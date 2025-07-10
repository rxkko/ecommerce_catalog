from decimal import Decimal
from sqlalchemy import String, Integer, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    image_url: Mapped[str] = mapped_column(String(255))
    product_category: Mapped[str] = mapped_column(String(50), index=True)

    in_carts: Mapped[list['CartItem']] = relationship('CartItem', back_populates='product')
    in_orders: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='product')

