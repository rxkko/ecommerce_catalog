from src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.product_repo import ProductRepository
from src.services.token_service import TokenService
from src.services.product_service import ProductService
from src.services.user_service import UserService
from src.repositories.user_repo import UserRepository
from src.core.config import settings
from fastapi import Depends


def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
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

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service)
) -> UserService:
    return UserService(user_repo, token_service)

def get_user_by_role(user: UserService = Depends(get_user_service)) -> bool:
    return user.is_admin if hasattr(user, 'is_admin') else False

# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     token_service: TokenService = Depends(get_token_service),
#     user_repo: UserRepository = Depends(get_user_repository)
# ):
#     try:
#         payload = token_service.verify_token(token)
#         user_id = payload.sub
#         user = await user_repo.get_user_by_id(int(user_id))
#         if user is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Пользователь не найден"
#             )
#         return user
#     except JWTError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Неверные учетные данные",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
