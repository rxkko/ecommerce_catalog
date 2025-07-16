from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, IntegrityError
from fastapi import HTTPException, status
from src.models.product import Product
from src.schemas.product import ProductBase, ProductUpdate, ProductCategory
from typing import Optional, List, Tuple
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class ProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_products(
        self, 
        limit: int = 10, 
        offset: int = 0
    ) -> Tuple[List[Product], int]:
        try:
            query = select(Product).order_by(Product.id).offset(offset).limit(limit)
            result = await self.session.execute(query)
            products = result.scalars().all()
            
            total = await self._get_total_products()
            return products, total
            
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении товаров: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении списка товаров"
            )

    async def _get_total_products(self) -> int:
        try:
            query = select(func.count()).select_from(Product)
            return (await self.session.execute(query)).scalar_one()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при подсчете товаров: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при подсчете товаров"
            )

    async def create_product(self, product_data: ProductBase) -> Product:
        try:
            product = Product(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                quantity=product_data.quantity,
                image_url=product_data.image_url,
                product_category=product_data.product_category
            )
            self.session.add(product)
            await self.session.commit()
            await self.session.refresh(product)
            return product
            
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Ошибка целостности при создании товара: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при создании товара (возможно, нарушение уникальности)"
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка БД при создании товара: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании товара"
            )

    async def update_product(
        self, 
        product_id: int, 
        product_data: ProductUpdate
    ) -> Product:
        try:
            product = await self.get_product_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Товар не найден"
                )

            update_data = product_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(product, field, value)

            await self.session.commit()
            await self.session.refresh(product)
            return product
            
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка при обновлении товара {product_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при обновлении товара"
            )

    async def delete_product(self, product_id: int) -> bool:
        try:
            product = await self.get_product_by_id(product_id)
            if not product:
                return False

            await self.session.delete(product)
            await self.session.commit()
            return True
            
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка при удалении товара {product_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при удалении товара"
            )

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        try:
            query = select(Product).where(Product.id == product_id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске товара {product_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при поиске товара"
            )
        
    async def get_products_by_ids(self, ids: List[int]) -> List[Product]:
        try:
            result = await self.session.execute(select(Product).where(Product.id.in_(ids)))
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске товаров")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при поиске товаров"
            )

    async def get_products_by_categories(
        self,
        categories: List[ProductCategory],
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        try:
            query = select(Product).where(
                Product.product_category.in_(categories)
            )
            
            if min_price is not None:
                query = query.where(Product.price >= min_price)
                
            if max_price is not None:
                query = query.where(Product.price <= max_price)

            result = await self.session.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            logger.error(f"Ошибка фильтрации товаров по категриям {categories}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка во время фильтрации товаров"
            )
        