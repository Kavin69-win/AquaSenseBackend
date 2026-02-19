from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.models.base import Base

class RecommendationLog(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    device_id = Column(String(50), index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # The Decision
    should_irrigate = Column(Boolean, nullable=False)
    reason_code = Column(String(50), nullable=False)  # e.g., "LOW_MOISTURE"
    confidence_score = Column(Float, default=1.0)
    
    # The Output
    message_sent = Column(String(255), nullable=False)  # Localized message sent