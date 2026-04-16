from app.extensions import db
from sqlalchemy import func
import uuid

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(uuid, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    sessions = db.relationship("Session",
                        back_populates="user",
                        cascade="all, delete-orphan", 
                        passive_deletes=True
                        )