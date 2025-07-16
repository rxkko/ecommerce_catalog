from fastapi import HTTPException, status
from src.repositories.cart_repo import CartRepository
from src.services.product_service import ProductService
from src.schemas.cart import CartResponse, CartCount
from src.schemas.product import ProductRead
import logging

logger = logging.getLogger(__name__)


class CartService:

    def __init__(self, cart_repo: CartRepository, product_service: ProductService):
        self.cart_repo = cart_repo
        self.product_service = product_service

    async def get_products_from_cart(self, user_id: int) -> CartResponse:
        try:
            print(user_id)
            cart_items = await self.cart_repo.get_products_from_cart(user_id)
            product_ids = [item.product_id for item in cart_items]
    
            products_db = await self.product_service.get_products_by_ids(product_ids)
            
            products = []
            total_price = 0.0

            for item in cart_items:
                product = next((p for p in products_db if p.id == item.product_id), None)
                if not product:
                    continue

                products.append(ProductRead(
                    id = item.product_id,
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    quantity=item.quantity,
                    image_url=product.image_url,
                    product_category=product.product_category
                ))
                total_price += float(product.price) * item.quantity
            return CartResponse(products=products, total_price=total_price)
        except Exception as e:
            logger.error(f"Ошибка при получении корзины в сервисах: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    async def get_cart_count(self, user_id: int) -> CartCount:
        try:
            count = await self.cart_repo.get_cart_count(user_id)
            return count
        except HTTPException as e:
            print(e)