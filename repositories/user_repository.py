from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.user import UserCreate

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: UserCreate):
    new_user = User(**user_data.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def update_user(db: Session, user_id: int, update_data: dict):
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    allowed_fields = {
        "nama",
        "email",
        "password",
        "role",
        "nim_nip",
        "no_hp",
        "foto",
    }

    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    db.delete(user)
    db.commit()

    return user