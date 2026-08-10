from pydantic import BaseModel


class UsageResponse(BaseModel):
    used: int
    limit: int
    remaining: int

    class Config:
        from_attributes = True
