from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.product import Product
from src.schemas.product import ProductBase, ProductUpdate, ProductCategory, ProductRead
from fastapi import Depends
from src.core.database import get_db
from typing import Annotated, Optional, List

class ProductRepository:
    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]):
        self.db = db

    async def get_products(self, limit: int = 10, offset: int = 0) -> tuple[list[Product], int]:
        products_query = select(Product).offset(offset).limit(limit)
        products_result = await self.db.execute(products_query)
        products = products_result.scalars().all()

        count_query = select(func.count()).select_from(Product)
        total = (await self.db.execute(count_query)).scalar_one()

        return products, total

    async def create_product(self, product_data: ProductBase) -> Product:
        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            quantity=product_data.quantity,
            image_url=product_data.image_url or None,
            product_category=product_data.product_category
        )
        
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product

    async def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        product = await self.get_product_by_id(product_id)
        update_data = product_data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(product, key, value)
            
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete_product(self, product_id: int) -> dict:
        product = await self.get_product_by_id(product_id)
        await self.db.delete(product)
        await self.db.commit()
        return {"message": f"Товар '{product.name}' успешно удален"}

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()
    
    async def get_product_by_category(self, category: ProductCategory) -> List[ProductRead]:
        result = await self.db.execute(select(Product).where(Product.product_category == category))
        products = result.scalars().all()
        return products
