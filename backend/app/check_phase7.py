from fastapi.testclient import TestClient
from sqlalchemy import text
from fastapi import HTTPException

from backend.app.main import app
from backend.app.db.session import SessionLocal

import backend.app.services.ocr_service as ocr_service
import backend.app.services.gemini_service as gemini_service
import backend.app.api.routes.pipeline as pipeline
from backend.app.core import config

client = TestClient(app)


def reset_db():
    with SessionLocal() as db:
        db.execute(text("DELETE FROM usages"))
        db.execute(text("DELETE FROM alerts"))
        db.execute(text("DELETE FROM prescriptions"))
        db.execute(text("DELETE FROM subscriptions"))
        db.execute(text("DELETE FROM users WHERE username LIKE 'phase7%'") )
        db.commit()


def stub_success_ocr(image_bytes: bytes) -> str:
    return "Stub OCR: Take Aspirin 100mg once daily."


def stub_success_summary(text: str) -> str:
    return "Stub Summary: Aspirin 100mg once daily."


def stub_medicines(text: str):
    return ["Aspirin"]


def stub_conditions(text: str):
    return ["Headache"]


def stub_warnings(text: str):
    return "Avoid with anticoagulants."


def stub_no_emergency(text: str):
    return False, "No emergency"


def stub_fail_ocr(image_bytes: bytes) -> str:
    raise HTTPException(status_code=502, detail="OCR failed")


def run_tests():
    reset_db()

    # patch success
    ocr_service.extract_text_from_image_bytes = stub_success_ocr
    gemini_service.summarize_text = stub_success_summary
    gemini_service.extract_medicines = stub_medicines
    gemini_service.identify_conditions = stub_conditions
    gemini_service.extract_warnings = stub_warnings
    gemini_service.assess_emergency_risk = stub_no_emergency
    # ensure pipeline's imported references are patched as well
    pipeline.extract_text_from_image_bytes = stub_success_ocr
    pipeline.summarize_text = stub_success_summary
    pipeline.extract_medicines = stub_medicines
    pipeline.identify_conditions = stub_conditions
    pipeline.extract_warnings = stub_warnings
    pipeline.assess_emergency_risk = stub_no_emergency

    results = {}

    # unauthenticated history request
    r = client.get("/prescriptions/")
    results['unauthenticated_history'] = (r.status_code == 401)

    # register two users
    reg1 = client.post("/auth/register", json={"username": "phase7user1", "email": "u1@example.com", "password": "Pass12345"})
    token1 = reg1.json().get('access_token')
    reg2 = client.post("/auth/register", json={"username": "phase7user2", "email": "u2@example.com", "password": "Pass12345"})
    token2 = reg2.json().get('access_token')

    # authenticated empty history
    r = client.get("/prescriptions/", headers={"Authorization": f"Bearer {token1}"})
    results['empty_history'] = (r.status_code == 200 and r.json() == [])

    # usage before any analysis
    r = client.get("/usage/", headers={"Authorization": f"Bearer {token1}"})
    usage_before = r.json()

    # successful analysis consumes usage
    up = client.post("/pipeline/upload", headers={"Authorization": f"Bearer {token1}"}, files={"file": ("t.jpg", b"bytes", "image/jpeg")})
    results['successful_analysis'] = (up.status_code == 200)

    r = client.get("/usage/", headers={"Authorization": f"Bearer {token1}"})
    usage_after = r.json()
    results['usage_consumed_on_success'] = (usage_after['used'] == usage_before['used'] + 1)

    # failed analysis should not consume usage
    ocr_service.extract_text_from_image_bytes = stub_fail_ocr
    pipeline.extract_text_from_image_bytes = stub_fail_ocr
    fail = client.post("/pipeline/upload", headers={"Authorization": f"Bearer {token1}"}, files={"file": ("t.jpg", b"bytes", "image/jpeg")})
    results['failed_analysis_no_consume'] = (fail.status_code != 200)
    r = client.get("/usage/", headers={"Authorization": f"Bearer {token1}"})
    results['usage_unchanged_after_failure'] = (r.json()['used'] == usage_after['used'])

    # restore success stub
    ocr_service.extract_text_from_image_bytes = stub_success_ocr
    pipeline.extract_text_from_image_bytes = stub_success_ocr
    pipeline.summarize_text = stub_success_summary
    pipeline.extract_medicines = stub_medicines
    pipeline.identify_conditions = stub_conditions
    pipeline.extract_warnings = stub_warnings

    # multiple prescriptions and ordering
    up_a = client.post("/pipeline/upload", headers={"Authorization": f"Bearer {token1}"}, files={"file": ("a.jpg", b"bytes", "image/jpeg")})
    up_b = client.post("/pipeline/upload", headers={"Authorization": f"Bearer {token1}"}, files={"file": ("b.jpg", b"bytes", "image/jpeg")})
    r = client.get("/prescriptions/", headers={"Authorization": f"Bearer {token1}"})
    if len(r.json()) >= 3:
        # print upload responses to help debug ordering issues
        print('DEBUG: up_a', up_a.status_code, up_a.json())
        print('DEBUG: up_b', up_b.status_code, up_b.json())
    pres = r.json()
    # check multiple and ordering by timestamp (newest first)
    results['multiple_and_ordering'] = False
    if len(pres) >= 3:
        try:
            results['multiple_and_ordering'] = pres[0]['created_at'] >= pres[1]['created_at']
        except Exception:
            results['multiple_and_ordering'] = False
    if not results['multiple_and_ordering']:
        print('DEBUG: prescriptions list:', pres)

    # retrieving own prescription
    first_id = pres[0]['id']
    r = client.get(f"/prescriptions/{first_id}", headers={"Authorization": f"Bearer {token1}"})
    results['retrieve_own'] = (r.status_code == 200 and r.json()['id'] == first_id)

    # another user's cannot access
    r = client.get(f"/prescriptions/{first_id}", headers={"Authorization": f"Bearer {token2}"})
    results['isolation'] = (r.status_code == 403)

    # missing prescription
    r = client.get("/prescriptions/999999", headers={"Authorization": f"Bearer {token1}"})
    results['missing_prescription'] = (r.status_code == 404)

    # usage limit enforcement
    # set small limit
    config.settings.free_analysis_limit = 1
    # consume for user2 once
    up = client.post("/pipeline/upload", headers={"Authorization": f"Bearer {token2}"}, files={"file": ("t.jpg", b"bytes", "image/jpeg")})
    up2 = client.post("/pipeline/upload", headers={"Authorization": f"Bearer {token2}"}, files={"file": ("t2.jpg", b"bytes", "image/jpeg")})
    print('DEBUG: user2 up status', up.status_code, 'up2 status', up2.status_code)
    results['limit_enforced'] = (up.status_code == 200 and up2.status_code == 402)
    if not results['limit_enforced']:
        print('DEBUG: up body:', up.json())
        print('DEBUG: up2 body:', up2.text)

    # page refresh does not consume usage (GET does not affect usage)
    r_get_before = client.get("/usage/", headers={"Authorization": f"Bearer {token1}"}).json()
    _ = client.get("/prescriptions/", headers={"Authorization": f"Bearer {token1}"})
    r_get_after = client.get("/usage/", headers={"Authorization": f"Bearer {token1}"}).json()
    results['get_no_consume'] = (r_get_before['used'] == r_get_after['used'])

    # run regressions: phase5 and phase6
    import subprocess, sys
    # run check_phase5
    cp5 = subprocess.run([sys.executable, "-m", "backend.app.check_phase5"], capture_output=True, text=True)
    cp6 = subprocess.run([sys.executable, "-m", "backend.app.check_phase6"], capture_output=True, text=True)
    results['phase5_regression'] = (cp5.returncode == 0)
    results['phase6_regression'] = (cp6.returncode == 0)

    # summary
    all_pass = all(results.values())
    print("PHASE 7 TEST RESULTS:")
    for k, v in results.items():
        print(f"{k}: {'PASS' if v else 'FAIL'}")
    print(f"ALL PASSED: {all_pass}")


if __name__ == '__main__':
    run_tests()
