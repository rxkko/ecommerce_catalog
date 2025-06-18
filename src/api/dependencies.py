from src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.product_repo import ProductRepository
from src.services.product_service import ProductService
from src.services.user_service import UserService
from src.repositories.user_repo import UserRepository
from fastapi import Depends


def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)

def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository)
) -> ProductService:
    return ProductService(product_repo)

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repo)

def get_user_by_role(user: UserService = Depends(get_user_service)) -> bool:
    return user.is_admin if hasattr(user, 'is_admin') else False