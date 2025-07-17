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
        result = await self.session.scalar(
            select(func.count(CartItem.id)).where(CartItem.user_id == user_id)
        )
        return result or 0
    
    async def add_product_to_cart(self, product_id: int, user_id: int):
        result = await self.session.execute()