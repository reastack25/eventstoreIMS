from models.user import User
from repositories.user_repo import UserRepository

class AuthService:

    @staticmethod
    def register(data):

        user = User(
            full_name=data["full_name"],
            email=data["email"],
            role="STORE_MANAGER"
        )

        user.set_password(
            data["password"]
        )

        return UserRepository.create(user)