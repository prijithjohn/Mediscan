from sqlalchemy.orm import Session

from backend.app.db.models.prescription import Prescription
from backend.app.schemas.prescription import PrescriptionCreate


def create_prescription(db: Session, user_id: int, payload: PrescriptionCreate) -> Prescription:
    prescription = Prescription(
        user_id=user_id,
        original_text=payload.original_text,
        summary=payload.summary,
        medicines=payload.medicines,
        dosage=payload.dosage,
        frequency=payload.frequency,
        duration=payload.duration,
        possible_conditions=payload.possible_conditions,
        warnings=payload.warnings,
    )
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription


def get_user_prescriptions(db: Session, user_id: int):
    # Order by id descending to reliably return newest prescriptions first
    return db.query(Prescription).filter(Prescription.user_id == user_id).order_by(Prescription.id.desc()).all()
