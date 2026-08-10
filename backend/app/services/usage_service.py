from datetime import date

from sqlalchemy.orm import Session

from backend.app.db.models.usage import Usage
from backend.app.core.config import settings


def get_today_usage(db: Session, user_id: int) -> Usage | None:
    today = date.today()
    return db.query(Usage).filter(Usage.user_id == user_id, Usage.usage_date == today).first()


def get_usage_summary(db: Session, user_id: int) -> dict:
    usage = get_today_usage(db, user_id)
    limit = settings.free_analysis_limit
    used = usage.used_count if usage else 0
    remaining = max(limit - used, 0)
    return {"used": used, "limit": limit, "remaining": remaining}


def can_consume(db: Session, user_id: int) -> bool:
    summary = get_usage_summary(db, user_id)
    return summary["used"] < summary["limit"]


def consume_usage(db: Session, user_id: int) -> None:
    today = date.today()
    usage = get_today_usage(db, user_id)
    if usage:
        usage.used_count += 1
    else:
        usage = Usage(user_id=user_id, usage_date=today, used_count=1, usage_limit=settings.free_analysis_limit)
        db.add(usage)
    db.commit()
    db.refresh(usage)
