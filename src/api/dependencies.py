from src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.product_repo import ProductRepository
from src.services.product_service import ProductService
from fastapi import Depends


def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)

def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository)
) -> ProductService:
    return ProductService(product_repo)

def get_user_by_role():
    # Placeholder for user role dependency
    pass