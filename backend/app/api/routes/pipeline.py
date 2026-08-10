from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db
from backend.app.schemas.prescription import PrescriptionCreate, PrescriptionResponse
from backend.app.services.alert_service import create_alert
from backend.app.services.gemini_service import (
    assess_emergency_risk,
    extract_medicines,
    extract_warnings,
    identify_conditions,
    summarize_text,
)
from backend.app.services.ocr_service import extract_text_from_image_bytes
from backend.app.services.prescription_service import create_prescription
from backend.app.services.usage_service import can_consume, consume_usage

MAX_UPLOAD_SIZE = 5 * 1024 * 1024

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/upload", response_model=PrescriptionResponse)
def process_prescription_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if file.content_type not in {"image/jpeg", "image/jpg", "image/png", "image/webp"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Upload a JPEG, PNG, or WEBP image.",
        )

    # enforce usage limits before heavy processing
    if not can_consume(db, current_user.id):
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Free analysis limit exceeded")

    image_bytes = file.file.read()
    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )
    if len(image_bytes) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Uploaded file exceeds the maximum allowed size of 5MB.",
        )

    extracted_text = extract_text_from_image_bytes(image_bytes)
    summary = summarize_text(extracted_text)
    medicines = extract_medicines(summary)
    possible_conditions = identify_conditions(summary)
    warnings = extract_warnings(summary)

    prescription_payload = PrescriptionCreate(
        original_text=extracted_text,
        summary=summary,
        medicines=medicines,
        possible_conditions=possible_conditions,
        warnings=warnings,
    )

    prescription = create_prescription(
        db,
        current_user.id,
        payload=prescription_payload,
    )

    # Only consume usage after successful processing and persistence
    try:
        consume_usage(db, current_user.id)
    except Exception:
        # non-fatal for processing; do not roll back prescription
        pass

    emergency, emergency_message = assess_emergency_risk(summary)
    if emergency and current_user.email:
        create_alert(
            db,
            user_id=current_user.id,
            prescription_id=prescription.id,
            subject="Emergency prescription alert",
            message=emergency_message,
            to_email=current_user.email,
        )

    return prescription
