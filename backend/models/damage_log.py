from extensions import db
from models.base import BaseModel

class DamageLog(BaseModel):
    __tablename__ = "damage_logs"

    item_id     = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    quantity    = db.Column(db.Integer, nullable=False)
    reason      = db.Column(db.Text)
    reported_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    item     = db.relationship("Item", backref="damage_logs")
    reporter = db.relationship("User", backref="damage_logs")