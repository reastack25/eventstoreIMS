
from extensions import db
from models.base import BaseModel

class JobCard(BaseModel):
    __tablename__ = "job_cards"

    reference    = db.Column(db.String(100), unique=True, nullable=False)
    # e.g. JC-001
    event_id     = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    assigned_to  = db.Column(db.Integer, db.ForeignKey("users.id"))
    status       = db.Column(db.String(50), default="DRAFT")
    notes        = db.Column(db.Text)
    created_by   = db.Column(db.Integer, db.ForeignKey("users.id"))

    assignee     = db.relationship("User", foreign_keys=[assigned_to], backref="assigned_job_cards")
    creator      = db.relationship("User", foreign_keys=[created_by], backref="created_job_cards")
    items        = db.relationship("JobCardItem", backref="job_card", lazy=True)

    def to_dict(self):
        return {
            "id":          self.id,
            "reference":   self.reference,
            "event_id":    self.event_id,
            "assigned_to": self.assigned_to,
            "status":      self.status,
            "notes":       self.notes,
            "created_by":  self.created_by,
            "created_at":  self.created_at.isoformat(),
            "items":       [i.to_dict() for i in self.items]
        }