from models.user import User
from extensions import db

class UserRepository:

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(
            email=email
        ).first()

    @staticmethod
    def create(user):
        db.session.add(user)
        db.session.commit()
        return user