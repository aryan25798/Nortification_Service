from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # email, sms, in-app
    message = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, sent, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
