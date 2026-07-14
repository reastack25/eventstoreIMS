# models/item.py

from extensions import db
from models.base import BaseModel

class Item(BaseModel):
    __tablename__ = "items"

    code        = db.Column(db.String(100), unique=True)
    name        = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    unit        = db.Column(db.String(50))
    quantity    = db.Column(db.Integer, default=0)
    available   = db.Column(db.Integer, default=0)
    status      = db.Column(db.String(50), default="ACTIVE")
    image_url   = db.Column(db.String(500))

    transactions = db.relationship("InventoryTransaction",backref="item",lazy=True,cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id":         self.id,
            "code":       self.code,
            "name":       self.name,
            "quantity":   self.quantity,
            "available":  self.available,
            "unit":       self.unit,
            "status":     self.status,
            "image_url":  self.image_url,
            "created_at": self.created_at.isoformat()
        }