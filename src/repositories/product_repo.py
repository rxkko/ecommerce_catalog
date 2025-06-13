from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.product import Product, ProductCategories
from src.schemas.product import ProductCreate, ProductUpdate
from fastapi import Depends
from src.core.database import get_db
from typing import Text, Annotated


class ProductRepository:
    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]):
        self.db = db

    async def get_products(self) -> list[Product]:
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def get_product_by_id(self, product_id: int) -> Product | None:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        if result is None:
            return None
        return result.scalar_one_or_none()

    async def create_product(self, product: ProductCreate) -> Product:
        new_product = ProductCreate(**product.model_dump())
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product

    async def update_product(self, product_id: int, product: ProductUpdate) -> Product | None:
        exiting_product = await self.get_product_by_id(product_id)
        if not exiting_product:
            return None
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(exiting_product, key, value)
        await self.db.commit()
        await self.db.refresh(exiting_product)
        return exiting_product
    
    async def delete_product(self, product_id: int) -> Text:
        product = await self.get_product_by_id(product_id)
        await self.db.delete(product)
        await self.db.commit()
        return f"Product {product.name} deleted successfully."

    async def get_product_by_category(self, category_id: int) -> list[Product]:
        result = await self.db.execute(select(ProductCategories)
                                       .where(ProductCategories.category_id == category_id)
                                       .join(Product, Product.id == ProductCategories.product_id))
        return result.scalars().all()