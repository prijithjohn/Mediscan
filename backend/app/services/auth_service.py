from datetime import timedelta
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, hash_password, verify_password
from backend.app.db.models.user import User
from backend.app.schemas.auth import TokenData, UserCreate, UserLogin


def register_user(db: Session, user_create: UserCreate) -> User:
    password_hash = hash_password(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        password_hash=password_hash,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, user_login: UserLogin) -> User | None:
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user or not verify_password(user_login.password, user.password_hash):
        return None
    return user


def create_user_token(user: User) -> str:
    access_token_expires = timedelta(minutes=30)
    return create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )


def get_user_from_token(db: Session, token_data: TokenData) -> User | None:
    if not token_data.username:
        return None
    return db.query(User).filter(User.username == token_data.username).first()
