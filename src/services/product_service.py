from typing import List, Optional
from decimal import Decimal
from fastapi import HTTPException, status
from src.models.product import Product
from src.schemas.product import (
    ProductBase, 
    ProductUpdate, 
    ProductRead,
    ProductCategory
)
from src.repositories.product_repo import ProductRepository
import logging

logger = logging.getLogger(__name__)

class ProductService:

    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get_product_by_id(self, product_id: int) -> ProductRead:
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            logger.warning(f"Продукт с ID {product_id} не найден")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Продукт не найден"
            )
        return product

    async def get_all_products(
        self, 
        limit: int = 10, 
        offset: int = 0
    ) -> dict:
        try:
            products, total = await self.product_repo.get_products(limit, offset)
            return {
                "items": products,
                "total": total,
                "page": (offset // limit) + 1 if limit > 0 else 1,
                "per_page": limit
            }
        except Exception as e:
            logger.error(f"Ошибка при получении продуктов: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении списка продуктов"
            )

    async def create_product(self, product_data: ProductBase) -> ProductRead:
        try:
            if product_data.price <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Цена должна быть положительной"
                )
                
            return await self.product_repo.create_product(product_data)
        except Exception as e:
            logger.error(f"Ошибка создания продукта: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при создании продукта: {str(e)}"
            )

    async def update_product(
        self, 
        product_id: int, 
        product_data: ProductUpdate
    ) -> ProductRead:
        try:
            product = await self.product_repo.update_product(product_id, product_data)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Продукт не найден"
                )
            return product
        except Exception as e:
            logger.error(f"Ошибка обновления продукта {product_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при обновлении продукта: {str(e)}"
            )

    async def delete_product(self, product_id: int) -> None:
        try:
            success = await self.product_repo.delete_product(product_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Продукт не найден"
                )
        except Exception as e:
            logger.error(f"Ошибка удаления продукта {product_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при удалении продукта: {str(e)}"
            )

    async def get_products_by_category(
        self, 
        category: ProductCategory
    ) -> List[ProductRead]:
        try:
            return await self.product_repo.get_products_by_category(category)
        except Exception as e:
            logger.error(f"Ошибка фильтрации по категории {category}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при фильтрации продуктов"
            )