from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PrescriptionCreate(BaseModel):
    original_text: str
    summary: Optional[str] = None
    medicines: Optional[List[str]] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    possible_conditions: Optional[List[str]] = None
    warnings: Optional[str] = None


class PrescriptionResponse(PrescriptionCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
