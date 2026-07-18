from extensions import db
from models.base import BaseModel

class InventoryTransaction(BaseModel):
    __tablename__ = "inventory_transactions"

    item_id          = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    quantity         = db.Column(db.Integer, nullable=False)
    reference_number = db.Column(db.String(100))
    remarks          = db.Column(db.Text)
    performed_by     = db.Column(db.Integer, db.ForeignKey("users.id"))

    def to_dict(self):
        return {
            "id":               self.id,
            "item_id":          self.item_id,
            "transaction_type": self.transaction_type,
            "quantity":         self.quantity,
            "reference_number": self.reference_number,
            "remarks":          self.remarks,
            "performed_by":     self.performed_by,
            "created_at":       self.created_at.isoformat()
        }
