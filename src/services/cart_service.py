from fastapi import HTTPException, status
from src.repositories.cart_repo import CartRepository
from src.schemas.cart import CartResponse
import logging

logger = logging.getLogger(__name__)


class CartService:

    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    async def get_products_from_cart(self, user_id: int) -> CartResponse:
        try:
            print(user_id)
            products = await self.cart_repo.get_products_from_cart(user_id)
            total_price = total_price = sum(product.price * product.quantity for product in products)
            return CartResponse(
                products=products,
                total_price=total_price
            )
        except Exception as e:
            logger.error(f"Ошибка при получении корзины: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Вы не авторизованы))"
            )
        