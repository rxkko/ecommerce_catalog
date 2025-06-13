from src.repositories.product_repo import ProductRepository


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get_product_by_id(self, product_id: int):
        return await self.product_repo.get_product_by_id(product_id)
    
    async def get_all_products(self):
        return await self.product_repo.get_products()
        
    async def create_product(self, product_data):
        return await self.product_repo.create_product(product_data)

    async def update_product(self, product_id, product_data):
        return await self.product_repo.update_product(product_id, product_data)

    async def delete_product(self, product_id):
        return await self.product_repo.delete_product(product_id)
