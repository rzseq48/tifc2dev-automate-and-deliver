from app.extensions import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.String(40), nullable=False)
    assigned_to = db.Column(db.String(80), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "assigned_to": self.assigned_to,
        }
