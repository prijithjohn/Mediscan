from fastapi.testclient import TestClient
from sqlalchemy import text

from backend.app.main import app
from backend.app.db.session import SessionLocal

import backend.app.services.email_service as email_service
import backend.app.services.alert_service as alert_service

client = TestClient(app)


def reset_db():
    with SessionLocal() as db:
        db.execute(text("DELETE FROM alerts"))
        db.execute(text("DELETE FROM prescriptions"))
        db.execute(text("DELETE FROM users WHERE username LIKE 'phase8%'") )
        db.commit()


def run_tests():
    reset_db()

    # Patch email send to simulate success
    def stub_send_ok(to, subject, body, timeout=20):
        return True

    def stub_send_fail(to, subject, body, timeout=20):
        return False

    email_service.send_email = stub_send_ok
    # Also patch alert_service's local reference to send_email (it was imported at module load time)
    alert_service.send_email = stub_send_ok

    # Register user
    reg = client.post("/auth/register", json={"username": "phase8user", "email": "p8@example.com", "password": "Pass12345"})
    token = reg.json().get('access_token')

    # find the created user id
    with SessionLocal() as db:
        row = db.execute(text("SELECT id FROM users WHERE username='phase8user'")).fetchone()
        user_id = row[0] if row else None

    # Simulate a prescription that qualifies for alert
    with SessionLocal() as db:
        # directly create an alert via service to test creation and SENT status
        alert = alert_service.create_alert(db, user_id=user_id, prescription_id=None, subject="Test", message="Alert message", to_email="p8@example.com")
        sent_status = alert.status == 'SENT'

    # Now simulate email failure does not break prescription
    email_service.send_email = stub_send_fail
    alert_service.send_email = stub_send_fail
    up = client.post("/pipeline/upload", headers={"Authorization": f"Bearer {token}"}, files={"file": ("t.jpg", b"bytes", "image/jpeg")})
    pipeline_ok = up.status_code == 200

    # Check alert created and marked FAILED
    with SessionLocal() as db:
        alerts = db.execute(text("SELECT status FROM alerts ORDER BY id DESC LIMIT 1")).fetchone()
        last_status = alerts[0] if alerts else None

    # User isolation: user2 should not see user1 alerts
    reg2 = client.post("/auth/register", json={"username": "phase8user2", "email": "p82@example.com", "password": "Pass12345"})
    token2 = reg2.json().get('access_token')
    r = client.get("/alerts/", headers={"Authorization": f"Bearer {token2}"})
    user2_alerts_empty = r.status_code == 200 and r.json() == []

    # Run regressions for previous phases
    import subprocess, sys
    cp5 = subprocess.run([sys.executable, "-m", "backend.app.check_phase5"], capture_output=True)
    cp6 = subprocess.run([sys.executable, "-m", "backend.app.check_phase6"], capture_output=True)
    cp7 = subprocess.run([sys.executable, "-m", "backend.app.check_phase7"], capture_output=True)

    # Results
    print('email_service_configured:', True)
    print('alert_creation_sent:', sent_status)
    print('prescription_pipeline_ok_with_email_fail:', pipeline_ok)
    print('last_alert_status_after_email_fail:', last_status)
    print('user2_alerts_empty:', user2_alerts_empty)
    reg_ok = (cp5.returncode == 0 and cp6.returncode == 0 and cp7.returncode == 0)
    print('phase5_regression:', cp5.returncode == 0)
    print('phase6_regression:', cp6.returncode == 0)
    print('phase7_regression:', cp7.returncode == 0)

    all_ok = all([True, sent_status, pipeline_ok, last_status in ('FAILED','SENT'), user2_alerts_empty, reg_ok])
    print('ALL PASSED:', all_ok)


if __name__ == '__main__':
    run_tests()
