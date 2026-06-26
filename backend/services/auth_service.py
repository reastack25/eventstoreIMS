from models.user import User
from repositories.user_repo import UserRepository
from extensions import db
from flask_jwt_extended import create_access_token

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

    @staticmethod
    def login(data):

        user = UserRepository.get_by_email(data["email"])

        if not user or not user.verify_password(data["password"]):
            return None, None

        if not user.is_active:
            return None, "Account is deactivated"

        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        return token, user