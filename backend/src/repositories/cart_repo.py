from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from src.models.cart_item import CartItem
import logging

logger = logging.getLogger(__name__)

class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_products_from_cart(self, user_id: int) -> list[CartItem]:
        try:
            products = await self.session.execute(select(CartItem).where(CartItem.user_id == user_id))
            products = products.scalars().all()
            print(products)
            return products
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении корзины: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении корзины"
            )
        
    async def get_cart_count(self, user_id: int) -> int:
        try:
            result = await self.session.scalar(
            select(func.count(CartItem.id)).where(CartItem.user_id == user_id)
            )
            return result or 0
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении количества товаров в корзине: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении количества товаров в корзине"
            )
    
    async def delete_product_from_cart(self, product_id: int, user_id: int):
        try:
            result = await self.session.execute(
                select(CartItem).where(
                    CartItem.product_id == product_id,
                    CartItem.user_id == user_id
                )
            )
            item = result.scalar_one_or_none()
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Товар не найден в корзине"
                )
            await self.session.delete(item)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении товара из корзины: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при удалении товара из корзины"
            )

    async def add_product_to_cart(self, product_id: int, user_id: int):
        result = await self.session.execute()