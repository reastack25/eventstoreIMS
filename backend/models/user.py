# models/user.py

from extensions import db
from models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    full_name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(50),nullable=False)
    is_active = db.Column(db.Boolean,default=True)