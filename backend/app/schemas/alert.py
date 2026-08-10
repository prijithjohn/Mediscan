from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr


AlertStatus = Literal["PENDING", "SENT", "FAILED"]


class AlertResponse(BaseModel):
    id: int
    user_id: int
    prescription_id: int | None
    email: EmailStr
    subject: str
    message: str
    status: AlertStatus
    sent_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
