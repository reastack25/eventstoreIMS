from extensions import db
from models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = db.Column(db.String(100),unique=True,nullable=False)
    description = db.Column(db.Text)

    items = db.relationship("Item",backref="category",lazy=True)

    def __repr__(self):
       return f"<Category {self.name}>"