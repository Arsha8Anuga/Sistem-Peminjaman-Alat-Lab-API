# app/middleware/auth_middleware.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.constants import HttpCode, ResponseMessage
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.utils.jwt_handler import verify_access_token
from app.repositories.user_repository import get_user_by_id
from app.constants.enums import UserRole

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah kadaluarsa",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak memiliki informasi pengguna",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(db, int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Pengguna tidak ditemukan",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def require_roles(*allowed_roles: UserRole):
  
    def _check(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Akses ditolak. "
                    f"Role '{current_user.role}' tidak diizinkan untuk endpoint ini."
                ),
            )
        return current_user

    return _check


def can_access_peminjaman(
    peminjaman,
    current_user,
):

    privileged_roles = {
        UserRole.ADMIN,
        UserRole.LABORAN,
        UserRole.ASISTEN,
    }

    if current_user.role in privileged_roles:
        return True

    if current_user.role == UserRole.MAHASISWA:

        if peminjaman.mahasiswa_id != current_user.id:

            raise HTTPException(
                status_code=HttpCode.FORBIDDEN,
                detail=ResponseMessage.FORBIDDEN,
            )

        return True

    raise HTTPException(
        status_code=HttpCode.FORBIDDEN,
        detail=ResponseMessage.FORBIDDEN,
    )