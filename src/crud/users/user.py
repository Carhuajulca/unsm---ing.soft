# src/crud/users.py
from sqlalchemy.orm import Session
from src.models.model import User
from src.schemas.users.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()