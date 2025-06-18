from fastapi import APIRouter, Depends, HTTPException, status
from src.api.dependencies import get_user_service, get_user_by_role
from src.schemas.user import UserCreate

router = APIRouter(tags=["user"])

@router.get("/me/{user_id}")
async def get_user_info(user_id: int, user_service = Depends(get_user_service)):
    return await user_service.get_user_info(user_id)

@router.post("/register")
async def register_user(user_data: UserCreate, user_service = Depends(get_user_service)):
    return await user_service.create_user(user_data)

@router.put("/update/{user_id}")
async def update_user(user_id: int, user_data: UserCreate, user_service = Depends(get_user_service)):
    return await user_service.update_user(user_id, user_data)

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, user_service = Depends(get_user_service)):
    return await user_service.delete_user(user_id)

@router.get("/all")
async def get_all_users(user_service = Depends(get_user_service)):
    return await user_service.get_all_users()

@router.get("/deactivate/{user_id}")
async def deactivate_user(user_id: int, is_admin: bool = Depends(get_user_by_role), user_service = Depends(get_user_service)):
    if is_admin:
        return await user_service.deactivate_user(user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для деактивации этого пользователя."
        )
