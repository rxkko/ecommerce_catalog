from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBearer
from src.models.user import User
from src.services.token_service import TokenService
from src.repositories.user_repo import UserRepository
from src.api.dependencies import get_token_service, get_user_repository
import logging

security = HTTPBearer()
logger = logging.getLogger(__name__)

async def get_current_user(
    request: Request,
    response: Response,
    token_service: TokenService = Depends(get_token_service),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    access_token = request.cookies.get("access_token")
    
    if access_token:
        try:
            payload = token_service.verify_token(access_token)
            user = await user_repo.get_user_by_id(int(payload.sub))
            
            if not user:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
            if not user.is_active:
                raise HTTPException(status.HTTP_403_FORBIDDEN, "Inactive user")
                
            return user
        except (KeyError, ValueError, HTTPException) as e:
            logger.debug(f"Access token error: {str(e)}")
        
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        try:
            refresh_result = await token_service.refresh_tokens(refresh_token, response)
            user = await user_repo.get_user_by_id(int(refresh_result["user_id"]))
            
            if not user or not user.is_active:
                raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid user")
                
            return user
        except (ValueError, HTTPException):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )

def admin_required(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user