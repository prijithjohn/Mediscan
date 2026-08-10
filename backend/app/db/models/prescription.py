from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    original_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    medicines = Column(JSON, nullable=True)
    dosage = Column(String(256), nullable=True)
    frequency = Column(String(256), nullable=True)
    duration = Column(String(256), nullable=True)
    possible_conditions = Column(JSON, nullable=True)
    warnings = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="prescriptions")
    alerts = relationship("Alert", back_populates="prescription", cascade="all, delete-orphan")
