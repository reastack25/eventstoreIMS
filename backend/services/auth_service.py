# services/auth_service.py

from models.user import User
from repositories.user_repo import UserRepository
from extensions import db
from flask_jwt_extended import create_access_token
from utils.roles import Role

class AuthService:

    @staticmethod
    def register(data):
        # Validate role
        role = data.get("role", Role.STORE_KEEPER)
        valid_roles = [Role.ADMIN, Role.STORE_MANAGER, Role.STORE_KEEPER, Role.SITE_MANAGER]

        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")

        user = User(
            full_name = data["full_name"],
            email     = data["email"],
            role      = role
        )
        user.set_password(data["password"])

        try:
            return UserRepository.create(user)
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def login(data):
        user = UserRepository.get_by_email(data["email"])

        if not user or not user.verify_password(data["password"]):
            return None, None

        if not user.is_active:
            return None, "Account is deactivated"

        token = create_access_token(
            identity = str(user.id),
            additional_claims = {"role": user.role}
        )

        return token, user