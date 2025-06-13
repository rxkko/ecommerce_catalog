from sqlalchemy import Integer, String, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from src.models.base import Base
from typing import TYPE_CHECKING

# Импорты для проверки типов, чтобы избежать циклических импортов во время выполнения
# if TYPE_CHECKING:
#     from src.models.category import Category

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String)

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="product_categories",
        back_populates="products",
    )

class ProductCategories(Base):
    __tablename__ = "product_categories"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)

from src.models.category import Category 