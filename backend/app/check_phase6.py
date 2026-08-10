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
    db.execute(text("DELETE FROM users WHERE username='phase6test'"))
    db.commit()

register_response = client.post(
    "/auth/register",
    json={
        "username": "phase6test",
        "email": "phase6test@example.com",
        "password": "StrongPass123",
    },
)
print("register status", register_response.status_code)
print("register body", register_response.json())
access_token = register_response.json().get("access_token")

if access_token:
    upload_response = client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {access_token}"},
        files={"file": ("test.jpg", b"fake-image-bytes", "image/jpeg")},
    )
    print("pipeline upload status", upload_response.status_code)
    print("pipeline upload body", upload_response.json())
else:
    print("no access token returned")
