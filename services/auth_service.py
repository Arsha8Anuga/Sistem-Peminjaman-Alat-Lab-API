from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user_repository import (
    get_user_by_email,
    create_user,
)

from app.schemas.user import UserRegister
from app.utils.hash import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.constants import HttpCode, ResponseMessage
from app.constants.enums import UserRole


# =========================================================
# LOGIN
# =========================================================
def login_user(db: Session, data):

    user = get_user_by_email(db, data.email)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=HttpCode.UNAUTHORIZED,
            detail=ResponseMessage.LOGIN_FAILED,
        )

    token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role.value,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# =========================================================
# REGISTER
# =========================================================
def register_user(db: Session, user_data: UserRegister):

    try:
        existing = get_user_by_email(db, user_data.email)

        if existing:
            raise HTTPException(
                status_code=HttpCode.CONFLICT,
                detail=ResponseMessage.EMAIL_TAKEN,
            )

        # build clean payload
        user_dict = user_data.model_dump()

        user_dict["password"] = hash_password(user_dict["password"])

        # ROLE DIPAKSA DI BACKEND
        user_dict["role"] = UserRole.MAHASISWA

        new_user = create_user(db, user_dict)

        db.commit()
        db.refresh(new_user)

        return new_user

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HttpCode.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )