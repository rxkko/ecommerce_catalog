from fastapi import APIRouter

router = APIRouter(tags=["user"])

@router.get("/user")
def get_user_info():
    return {"message": "User information retrieved successfully"}