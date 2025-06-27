from fastapi import APIRouter, Depends, Cookie, Response, HTTPException, status
from src.services.token_service import TokenService
from src.repositories.user_repo import UserRepository
from src.api.dependencies import get_token_service, get_user_repository
from src.schemas.product import ProductCategory

router = APIRouter(tags=["token"])

@router.post("/refresh")
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None),
    token_service: TokenService = Depends(get_token_service),
    user_repo: UserRepository = Depends(get_user_repository)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token отсутствует"
        )