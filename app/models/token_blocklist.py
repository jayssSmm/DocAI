from app.extensions import Base
from sqlalchemy import Column,Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship

class TokenBlocklist(Base):
    id = Column(Integer, primary_key=True)
    jti = Column(String(36), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    