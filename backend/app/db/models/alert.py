from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from backend.app.db.base import Base

ALERT_STATUS_PENDING = "PENDING"
ALERT_STATUS_SENT = "SENT"
ALERT_STATUS_FAILED = "FAILED"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id", ondelete="SET NULL"), nullable=True)
    email = Column(String(256), nullable=False)
    subject = Column(String(256), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(64), nullable=False, default=ALERT_STATUS_PENDING)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="alerts")
    prescription = relationship("Prescription", back_populates="alerts")
