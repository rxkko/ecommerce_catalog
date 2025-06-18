from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, func
from src.models.product import Product, ProductCategories
from src.schemas.product import ProductBase, ProductUpdate
from fastapi import Depends
from src.core.database import get_db
from typing import Annotated


class ProductRepository:
    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]):
        self.db = db

    async def get_products(self, limit: int = 10, offset: int = 0) -> tuple[list[Product], int]:
        """Получение всех продуктов. Возвращает пустой список при отсутствии данных."""
        try:
            query = select(Product).offset(offset).limit(limit)
            result = await self.db.execute(query)
            products = result.scalars().all()
            total_query = select(func.count()).select_from(Product)
            total = (await self.db.execute(total_query)).scalar_one()
            return products, total
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка базы данных при получении всех товаров: {str(e)}")

    async def get_product_by_id(self, product_id: int) -> Product | None:
        """Получение продукта по ID. Возвращает None если продукт не найден."""
        try:
            result = await self.db.execute(
                select(Product).where(Product.id == product_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка базы данных при получении товара по ID: {str(e)}")

    async def create_product(self, product: ProductBase) -> Product:
        """Создание нового продукта с обработкой ошибок уникальности."""
        try:
            new_product = Product(
                name=product.name,
                description=product.description,
                price=product.price,
                quantity=product.quantity,
                image_url=product.image_url if product.image_url else None
            )
            self.db.add(new_product)
            await self.db.commit()
            await self.db.refresh(new_product)
            return new_product
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(f"Товар '{product.name}' уже существует")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise ValueError(f"Ошибка базы данных при создании товара: {str(e)}")

    async def update_product(self, product_id: int, product_update: ProductUpdate) -> Product | None:
        """Обновление продукта. Возвращает None если продукт не найден."""
        try:
            existing_product = await self.get_product_by_id(product_id)
            if not existing_product:
                return None
            update_data = product_update.model_dump(exclude_unset=True, exclude_none=True)
            for key, value in update_data.items():
                setattr(existing_product, key, value)   
            await self.db.commit()
            await self.db.refresh(existing_product)
            return existing_product
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(f"Ошибка целостности при обновлении товара: {str(e)}")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise ValueError(f"Ошибка базы данных при обновлении товара: {str(e)}")

    async def delete_product(self, product_id: int) -> str:
        """Удаление продукта с обработкой ошибок ссылочной целостности."""
        try:
            product = await self.get_product_by_id(product_id)
            if not product:
                raise ValueError("Товар не найден")

            await self.db.delete(product)
            await self.db.commit()
            return f"Продукт {product.name} успешно удалён."
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("Невозможно удалить продукт, так как он используется в других таблицах.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise ValueError(f"Ошибка базы данных при удалении товара: {str(e)}")

    async def get_product_by_category(self, category_id: int) -> list[Product]:
        """Получение продуктов по категории. Возвращает пустой список при отсутствии."""
        try:
            result = await self.db.execute(
                select(ProductCategories)
                .where(ProductCategories.category_id == category_id)
                .join(Product, Product.id == ProductCategories.product_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка базы данных при получении товаров по категории: {str(e)}")
