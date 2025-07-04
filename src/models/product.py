from sqlalchemy import Integer, String, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from src.models.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String)
    product_category: Mapped[str] = mapped_column(String)