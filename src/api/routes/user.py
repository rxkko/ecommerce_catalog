from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Request
from pydantic import EmailStr
from typing import Annotated
from src.api.dependencies import get_user_service, get_user_by_role, get_token_service, get_user_repository
from src.repositories.user_repo import UserRepository
from src.services.token_service import TokenService
from src.schemas.user import UserCreate, LoginRequest
from src.services.user_service import UserService
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["user"])
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
templates = Jinja2Templates(directory="src/frontend/templates")

@router.post("/login")
async def login_user(
    request: LoginRequest,
    user_service: UserServiceDep,
    response: Response
):
    print(request.email, request.password)
    return await user_service.login(request.email, request.password, response)

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Успешный выход"}

@router.get("/register")
async def register_user(request: Request):
    return templates.TemplateResponse(
            "registration.html",
            {"request": request}
        )

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
