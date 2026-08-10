from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.models.alert import Alert, ALERT_STATUS_FAILED, ALERT_STATUS_PENDING, ALERT_STATUS_SENT
from backend.app.services.email_service import send_email


def create_alert(
    db: Session,
    user_id: int,
    prescription_id: int | None,
    subject: str,
    message: str,
    to_email: str | None = None,
) -> Alert:
    recipient = to_email or settings.alert_email or settings.email_sender
    alert = Alert(
        user_id=user_id,
        prescription_id=prescription_id,
        email=recipient,
        subject=subject,
        message=message,
        status=ALERT_STATUS_PENDING,
        created_at=datetime.utcnow(),
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    # Attempt to send the email if a recipient is configured. Failures should not break prescription save.
    if recipient:
        try:
            sent = send_email(recipient, subject, message)
            if sent:
                alert.status = ALERT_STATUS_SENT
                alert.sent_at = datetime.utcnow()
            else:
                alert.status = ALERT_STATUS_FAILED
            db.commit()
            db.refresh(alert)
        except Exception:
            alert.status = ALERT_STATUS_FAILED
            db.commit()
            db.refresh(alert)

    return alert
