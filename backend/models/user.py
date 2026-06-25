# models/user.py

from extensions import db
from models.base import BaseModel
from werkzeug.security import (generate_password_hash,check_password_hash)

class User(BaseModel):
    __tablename__ = "users"

    full_name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(50),nullable=False)
    is_active = db.Column(db.Boolean,default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(
            self.password_hash,password
        )