from fastapi.testclient import TestClient
from sqlalchemy import text

from backend.app.main import app
from backend.app.db.session import SessionLocal

# Import services to patch
import backend.app.services.ocr_service as ocr_service
import backend.app.services.gemini_service as gemini_service
import backend.app.api.routes.pipeline as pipeline

client = TestClient(app)

# Patch external calls with deterministic stubs

def _stub_extract_text(image_bytes: bytes) -> str:
    return "Stubbed OCR detected: Take Paracetamol 500mg twice daily."


def _stub_summarize(text: str) -> str:
    return "Stubbed summary: Paracetamol 500mg twice daily."


def _stub_extract_medicines(text: str) -> list:
    return ["Paracetamol"]


def _stub_identify_conditions(text: str) -> list:
    return ["Fever"]


def _stub_extract_warnings(text: str) -> str:
    return "Take with food. Avoid alcohol."


def _stub_assess_emergency(text: str):
    return False, "No immediate emergency detected."

# Apply patches
ocr_service.extract_text_from_image_bytes = _stub_extract_text
gemini_service.summarize_text = _stub_summarize
gemini_service.extract_medicines = _stub_extract_medicines
gemini_service.identify_conditions = _stub_identify_conditions
gemini_service.extract_warnings = _stub_extract_warnings
gemini_service.assess_emergency_risk = _stub_assess_emergency

# Patch pipeline's imported references (they were imported at module import time)
pipeline.extract_text_from_image_bytes = _stub_extract_text
pipeline.summarize_text = _stub_summarize
pipeline.extract_medicines = _stub_extract_medicines
pipeline.identify_conditions = _stub_identify_conditions
pipeline.extract_warnings = _stub_extract_warnings
pipeline.assess_emergency_risk = _stub_assess_emergency

# Clean DB
with SessionLocal() as db:
    db.execute(text("DELETE FROM usages"))
    db.execute(text("DELETE FROM alerts"))
    db.execute(text("DELETE FROM prescriptions"))
    db.execute(text("DELETE FROM subscriptions"))
    db.execute(text("DELETE FROM users WHERE username='phase6final'"))
    db.commit()

# Register user
register_response = client.post(
    "/auth/register",
    json={
        "username": "phase6final",
        "email": "phase6final@example.com",
        "password": "FinalTestPass123",
    },
)
print("register status", register_response.status_code)
print("register body", register_response.json())
access_token = register_response.json().get("access_token")

# Run pipeline upload
if access_token:
    upload_response = client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {access_token}"},
        files={"file": ("test.jpg", b"stub-image-bytes", "image/jpeg")},
    )
    print("pipeline upload status", upload_response.status_code)
    print("pipeline upload body", upload_response.json())

    # Verify persistence using DB
    with SessionLocal() as db:
        res = db.execute(text("SELECT count(*) FROM prescriptions WHERE id>0"))
        count = res.scalar_one()
        print("prescription count in DB", count)
else:
    print("no access token returned")
