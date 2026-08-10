from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.db.models.user import User
from backend.app.schemas.auth import Token, UserCreate, UserLogin
from backend.app.services.auth_service import (
    authenticate_user,
    create_user_token,
    register_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user = register_user(db, user_create)
    access_token = create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_login = UserLogin(username=form_data.username, password=form_data.password)
    user = authenticate_user(db, user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
