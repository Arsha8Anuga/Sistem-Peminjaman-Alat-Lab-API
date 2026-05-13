from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.constants import HttpCode, ResponseMessage
from app.utils.hash import hash_password


# ---------------------------------------------------------------------
# READ
# ---------------------------------------------------------------------

def get_all_users(db: Session):
    return user_repository.get_all_users(db)


def get_user_by_id(db: Session, user_id: int):
    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.USER_NOT_FOUND,
        )

    return user


def update_user(db: Session, user_id: int, update_data: dict):

    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(HttpCode.NOT_FOUND, ResponseMessage.USER_NOT_FOUND)

    try:
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        if "email" in update_data and update_data["email"] != user.email:
            existing = user_repository.get_user_by_email(db, update_data["email"])
            if existing:
                raise HTTPException(HttpCode.CONFLICT, ResponseMessage.EMAIL_TAKEN)

        updated = user_repository.update_user(db, user_id, update_data)

        db.commit()
        db.refresh(updated)

        return updated

    except Exception:
        db.rollback()
        raise


def delete_user(db: Session, user_id: int):

    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(HttpCode.NOT_FOUND, ResponseMessage.USER_NOT_FOUND)

    try:
        deleted = user_repository.delete_user(db, user_id)

        db.commit()

        return deleted

    except Exception:
        db.rollback()
        raise