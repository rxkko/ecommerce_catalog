from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.dependencies.db_deps import get_db
from src.repositories.product_repo import ProductRepository
from src.repositories.user_repo import UserRepository
from src.services.product_service import ProductService
from src.services.token_service import TokenService
from src.services.user_service import UserService
from src.services.cart_service import CartService


def get_product_repository(
    db: AsyncSession = Depends(get_db)
) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository)
) -> ProductService:
    return ProductService(product_repo)


def get_token_service() -> TokenService:
    return TokenService(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )


def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepository:
    return UserRepository(db)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service)
) -> UserService:
    return UserService(user_repo, token_service)

def get_cart_service(
        db: AsyncSession = Depends(get_db)
):
    return CartService(db)