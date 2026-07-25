from extensions import db
from models.base import BaseModel

class DamageLog(BaseModel):
    __tablename__ = "damage_logs"

    item_id      = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    quantity     = db.Column(db.Integer, nullable=False)
    reason       = db.Column(db.Text)
    reported_by  = db.Column(db.Integer, db.ForeignKey("users.id"))
    estimated_cost = db.Column(db.Float, default=0)
    job_card_ref = db.Column(db.String(100))

    item     = db.relationship("Item", backref="damage_logs")
    reporter = db.relationship("User", backref="reported_damages")

    def to_dict(self):
        return {
            "id":             self.id,
            "item_id":        self.item_id,
            "item_name":      self.item.name if self.item else None,
            "item_code":      self.item.code if self.item else None,
            "quantity":       self.quantity,
            "reason":         self.reason,
            "reported_by":    self.reported_by,
            "reporter_name":  self.reporter.full_name if self.reporter else None,
            "estimated_cost": self.estimated_cost,
            "job_card_ref":   self.job_card_ref,
            "created_at":     self.created_at.isoformat()
        }
