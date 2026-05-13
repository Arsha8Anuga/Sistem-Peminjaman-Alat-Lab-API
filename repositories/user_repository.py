from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.user import UserRegister


def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict):
    new_user = User(**user_data)
    db.add(new_user)
    return new_user


def update_user(db: Session, user_id: int, update_data: dict):
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    for key, value in update_data.items():
        setattr(user, key, value)

    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    db.delete(user)
    return user