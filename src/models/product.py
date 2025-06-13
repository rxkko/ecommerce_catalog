from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship

from .base import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    price = Column(Numeric(10, 2))
    quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
    image_url = Column(String)