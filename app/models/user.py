from app.extensions import db
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("gen_random_uuid()"))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    sessions = db.relationship("Session",
                        back_populates="user",
                        cascade="all, delete-orphan", 
                        passive_deletes=True
                        )