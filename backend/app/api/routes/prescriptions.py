from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db
from backend.app.db.models.prescription import Prescription
from backend.app.schemas.prescription import PrescriptionCreate, PrescriptionResponse
from backend.app.services.prescription_service import create_prescription, get_user_prescriptions

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])


@router.post("/", response_model=PrescriptionResponse)
def add_prescription(
    payload: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_prescription(db, current_user.id, payload)


@router.get("/", response_model=list[PrescriptionResponse])
def list_prescriptions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_user_prescriptions(db, current_user.id)


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(prescription_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
    if prescription.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this prescription")
    return prescription
