from backend.app.db.session import SessionLocal
from backend.app.db.models.alert import Alert, ALERT_STATUS_SENT, ALERT_STATUS_FAILED
from backend.app.services.alert_service import create_alert


def test_create_alert_status_sent(monkeypatch):
    def fake_send_email(to_email, subject, body, timeout=20):
        return True

    monkeypatch.setattr("backend.app.services.alert_service.send_email", fake_send_email)
    with SessionLocal() as db:
        alert = create_alert(
            db,
            user_id=1,
            prescription_id=None,
            subject="Test",
            message="Test message",
            to_email="test@example.com",
        )
        assert alert is not None
        assert alert.status == ALERT_STATUS_SENT


def test_create_alert_status_failed(monkeypatch):
    def fake_send_email(to_email, subject, body, timeout=20):
        return False

    monkeypatch.setattr("backend.app.services.alert_service.send_email", fake_send_email)
    with SessionLocal() as db:
        alert = create_alert(
            db,
            user_id=1,
            prescription_id=None,
            subject="Test",
            message="Test message",
            to_email="test@example.com",
        )
        assert alert is not None
        assert alert.status == ALERT_STATUS_FAILED
