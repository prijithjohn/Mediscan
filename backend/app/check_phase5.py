from fastapi.testclient import TestClient
from sqlalchemy import text

from backend.app.main import app
from backend.app.db.session import SessionLocal

client = TestClient(app)

with SessionLocal() as db:
    db.execute(text("DELETE FROM usages"))
    db.execute(text("DELETE FROM alerts"))
    db.execute(text("DELETE FROM prescriptions"))
    db.execute(text("DELETE FROM subscriptions"))
    db.execute(text("DELETE FROM users WHERE username='phase5test'"))
    db.commit()

register_response = client.post(
    "/auth/register",
    json={
        "username": "phase5test",
        "email": "phase5test@example.com",
        "password": "StrongPass123",
    },
)
print("register status", register_response.status_code)
print("register body", register_response.json())
access_token = register_response.json().get("access_token")
if access_token:
    response = client.get(
        "/prescriptions/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print("prescriptions status", response.status_code)
    print("prescriptions body", response.json())
else:
    print("no access token returned")
