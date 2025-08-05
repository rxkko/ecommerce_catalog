from fastapi import HTTPException, status
from src.services.cart_service import CartService
from src.repositories.order_repo import OrderRepository
from src.schemas.order import OrderResponse

class OrderService():
    def __init__(self, order_repo: OrderRepository, cart_service: CartService):
        self.order_repo = order_repo
        self.cart_service = cart_service

    async def make_order(self, user_id: int) -> OrderResponse:
        try:
            cart_items = self.cart_service.get_products_from_cart(user_id)
            order = self.order_repo.make_order(cart_items)
            return order
        except HTTPException as e:
            raise e