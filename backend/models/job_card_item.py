from extensions import db
from models.base import BaseModel

class JobCardItem(BaseModel):
    __tablename__ = "job_card_items"

    job_card_id        = db.Column(db.Integer, db.ForeignKey("job_cards.id"), nullable=False)
    item_id            = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    quantity_requested = db.Column(db.Integer, nullable=False)
    quantity_returned  = db.Column(db.Integer, default=0)
    quantity_damaged   = db.Column(db.Integer, default=0)

    item = db.relationship("Item", backref="job_card_items")

    def to_dict(self):
        return {
            "id":                 self.id,
            "job_card_id":        self.job_card_id,
            "item_id":            self.item_id,
            "item_name":          self.item.name if self.item else None,
            "quantity_requested": self.quantity_requested,
            "quantity_returned":  self.quantity_returned,
            "quantity_damaged":   self.quantity_damaged,
        }
