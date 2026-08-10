from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, get_current_user
from backend.app.services.usage_service import get_usage_summary

router = APIRouter(prefix="/usage", tags=["usage"])


@router.get("/", response_model=dict)
def usage_summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_usage_summary(db, current_user.id)
