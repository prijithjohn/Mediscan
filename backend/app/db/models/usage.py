from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class Usage(Base):
    __tablename__ = "usages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    usage_date = Column(Date, nullable=False)
    used_count = Column(Integer, nullable=False, default=0)
    usage_limit = Column(Integer, nullable=False, default=10)

    user = relationship("User", back_populates="usages")
