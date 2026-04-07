from app.extensions import db
from sqlalchemy import func

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String, nullable=False)
    is_statefull = db.Column(db.Boolean, default=False)
    created_at = created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
    db.CheckConstraint(
        "role IN ('user', 'assistant')",
        name="check_role_valid"
    ),)

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role":self.role,
            "content": self.content,
        }

    sessions = db.relationship('Session', back_populates='messages')
