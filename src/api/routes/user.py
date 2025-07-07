from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.templating import Jinja2Templates
from typing import Annotated

from src.api.dependencies import get_user_service
from src.schemas.user import UserCreate, UserUpdate, LoginRequest
from src.services.user_service import UserService
from src.models.user import User
from src.dependencies.auth_deps import admin_required, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
templates = Jinja2Templates(directory="src/frontend/templates")


@router.post(
    "/login",
    summary="Аутентификация пользователя"
)
async def login(
    credentials: LoginRequest,
    response: Response,
    user_service: UserServiceDep
):
    return await user_service.login(credentials.email, credentials.password, response)


@router.post(
    "/logout",
    summary="Выход из системы"
)
async def logout(response: Response):
    """Очищает cookies с токенами."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logout successful"}


@router.get(
    "/register",
    include_in_schema=False
)
async def register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя"
)
async def register(
    user_data: UserCreate,
    user_service: UserServiceDep
):
    return await user_service.create_user(user_data)


@router.put(
    "/{user_id}",
    summary="Обновление данных пользователя"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserServiceDep,
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для изменения этого пользователя"
        )
    return await user_service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление пользователя"
)
async def delete_user(
    user_id: int,
    user_service: UserServiceDep,
    _: User = Depends(admin_required)
):
    await user_service.delete_user(user_id)
    return None


@router.get(
    "/",
    summary="Получение списка пользователей"
)
async def get_all_users(user_service: UserServiceDep):
    return await user_service.get_users()


@router.post(
    "/{user_id}/deactivate",
    summary="Деактивация пользователя",
    status_code=status.HTTP_204_NO_CONTENT
)
async def deactivate_user(
    user_id: int,
    user_service: UserServiceDep,
    _: User = Depends(admin_required)
):
    await user_service.deactivate_user(user_id)
    return None