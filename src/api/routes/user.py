from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from pydantic import EmailStr
from typing import Annotated
from src.api.dependencies import get_user_service, get_user_by_role, get_token_service, get_user_repository
from src.repositories.user_repo import UserRepository
from src.services.token_service import TokenService
from src.schemas.user import UserCreate
from src.services.user_service import UserService

router = APIRouter(tags=["user"])
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

@router.post("/login")
async def login_user(
    email: EmailStr,
    password: str,
    user_service: UserServiceDep,
    response: Response
):
    return await user_service.login(email, password, response)

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Успешный выход"}

@router.post("/register")
async def register_user(user_data: UserCreate, user_service: UserServiceDep):
    return await user_service.create_user(user_data)

@router.put("/update/{user_id}")
async def update_user(user_id: int, user_data: UserCreate, user_service: UserServiceDep):
    return await user_service.update_user(user_id, user_data)

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, user_service: UserServiceDep):
    return await user_service.delete_user(user_id)

@router.get("/all")
async def get_all_users(user_service: UserServiceDep):
    return await user_service.get_users()

@router.get("/deactivate/{user_id}")
async def deactivate_user(user_id: int, user_service: UserServiceDep, is_admin: bool = Depends(get_user_by_role)):
    if is_admin:
        return await user_service.deactivate_user(user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для деактивации этого пользователя."
        )
