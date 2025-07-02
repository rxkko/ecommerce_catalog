from src.models.product import Product
from src.schemas.product import ProductBase, ProductUpdate, ProductRead, ProductCategory
from src.repositories.product_repo import ProductRepository
from typing import List


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get_product_by_id(self, product_id: int) -> Product:
        return await self.product_repo.get_product_by_id(product_id)
    
    async def get_all_products(self, limit: int = 10, offset: int = 0) -> dict:
        products, total = await self.product_repo.get_products(limit=limit, offset=offset)
        return {
            "items": products,
            "total": total,
            "page": (offset // limit) + 1 if limit > 0 else 1,
            "per_page": limit
        }
        
    async def create_product(self, product_data: ProductBase) -> Product:
        return await self.product_repo.create_product(product_data)

    async def update_product(self, 
                           product_id: int, 
                           product_data: ProductUpdate) -> Product:
        return await self.product_repo.update_product(product_id, product_data)

    async def delete_product(self, product_id: int) -> dict:
        return await self.product_repo.delete_product(product_id)
    
    async def get_product_by_category(self, category: ProductCategory) -> List[ProductRead]:
        return await self.product_repo.get_product_by_category(category)