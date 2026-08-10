from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, nullable=False, index=True)
    email = Column(String(256), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    prescriptions = relationship(
        "Prescription",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    subscriptions = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    usages = relationship(
        "Usage",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    alerts = relationship(
        "Alert",
        back_populates="user",
        cascade="all, delete-orphan",
    )
