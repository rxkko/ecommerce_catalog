from src.repositories.product_repo import ProductRepository
from fastapi import HTTPException, status
from src.models.product import Product
from src.schemas.product import ProductBase, ProductUpdate
from src.models.user import User


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get_product_by_id(self, product_id: int) -> Product:
        """Получение товара с проверкой его существования"""
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )
        return product
    
    async def get_all_products(self, page: int = 1, per_page: int = 10) -> dict:
        """Получение товаров с пагинацией"""
        products = await self.product_repo.get_products()
        start = (page - 1) * per_page
        end = start + per_page
        return {
            "items": products[start:end],
            "total": len(products),
            "page": page,
            "per_page": per_page
        }
        
    async def create_product(self, product_data: ProductBase) -> Product:
        """Создание товара с валидацией данных"""
        if product_data.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Цена должна быть положительной"
            )
        
        if len(product_data.name) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Название должно содержать минимум 3 символа"
            )
            
        return await self.product_repo.create_product(product_data)

    async def update_product(self, 
                           product_id: int, 
                           product_data: ProductUpdate) -> Product:
        """Обновление товара с валидацией"""
        if product_data.price is not None and product_data.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Цена должна быть положительной"
            )
            
        updated_product = await self.product_repo.update_product(product_id, product_data)
        if not updated_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )
        return updated_product

    async def delete_product(self, product_id: int, user: User) -> str:
        """Удаление товара с проверкой наличия заказов"""
        product = await self.get_product_by_id(product_id)
        if product.orders_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Нельзя удалить товар с существующими заказами"
            )
            
        return await self.product_repo.delete_product(product_id)