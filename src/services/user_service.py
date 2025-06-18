from src.core.security import get_password_hash, verify_password
from src.schemas.user import UserCreate, UserUpdate, UserRead

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id):
        return self.user_repository.get_user_by_id(user_id)

    def create_user(self, user_data: UserCreate):
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        return self.user_repository.create_user(user_dict)

    def update_user(self, user_id, user_data):
        return self.user_repository.update_user(user_id, user_data)

    def delete_user(self, user_id):
        return self.user_repository.delete_user(user_id)