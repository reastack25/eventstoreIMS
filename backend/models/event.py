
from extensions import db
from models.base import BaseModel

class Event(BaseModel):
    __tablename__ = "events"

    name         = db.Column(db.String(255), nullable=False)
    client_name  = db.Column(db.String(255))
    event_date   = db.Column(db.Date, nullable=False)
    venue        = db.Column(db.String(255))
    status       = db.Column(db.String(50), default="UPCOMING")
    created_by   = db.Column(db.Integer, db.ForeignKey("users.id"))

    creator      = db.relationship("User", backref="events")
    job_cards    = db.relationship("JobCard", backref="event", lazy=True)

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "client_name": self.client_name,
            "event_date":  self.event_date.isoformat(),
            "venue":       self.venue,
            "status":      self.status,
            "created_by":  self.created_by,
            "created_at":  self.created_at.isoformat()
        }