from extensions import db
from models.base import BaseModel

class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action  = db.Column(db.String(100), nullable=False)  # RECEIVE_STOCK, DISPATCH_STOCK, etc.
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))

    # Relationship
    user = db.relationship("User", backref="audit_logs")

    def to_dict(self):
        return {
            "id":         self.id,
            "user_id":    self.user_id,
            "action":     self.action,
            "details":    self.details,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat()
        }