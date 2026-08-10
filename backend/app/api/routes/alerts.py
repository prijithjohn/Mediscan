from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, get_current_user
from backend.app.db.models.alert import Alert
from backend.app.schemas.alert import AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=list[AlertResponse])
def list_alerts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    alerts = db.query(Alert).filter(Alert.user_id == current_user.id).order_by(Alert.id.desc()).all()
    return [AlertResponse.model_validate(alert) for alert in alerts]


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    if alert.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this alert")
    return AlertResponse.model_validate(alert)
