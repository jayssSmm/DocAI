from app.extensions import db
from sqlalchemy import func

class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    title = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    user = db.relationship("User", back_populates="sessions")

    messages = db.relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan"
    )