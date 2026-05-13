# app/middleware/auth_middleware.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.utils.jwt_handler import verify_access_token
from app.repositories.user_repository import get_user_by_id
from app.constants.enums import UserRole

# =========================================================
# Bearer token scheme
# =========================================================

security = HTTPBearer()


# =========================================================
# GET CURRENT USER
# Dependency: verifikasi token JWT dan kembalikan objek user
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Dependency untuk mendapatkan user yang sedang login.

    Cara kerja:
    1. Ambil Bearer token dari header Authorization
    2. Decode & verifikasi token via verify_access_token()
    3. Ambil user dari database berdasarkan 'sub' di payload
    4. Kembalikan objek User

    Raises:
        401 - Token tidak ada, tidak valid, atau sudah expired
        401 - User tidak ditemukan di database
    
    Contoh pemakaian di route:
        current_user = Depends(get_current_user)
    """
    token = credentials.credentials

    # Decode token — verify_access_token mengembalikan None jika gagal
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah kadaluarsa",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ambil user_id dari payload (disimpan sebagai "sub" saat token dibuat)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak memiliki informasi pengguna",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ambil user dari database
    user = get_user_by_id(db, int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Pengguna tidak ditemukan",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# =========================================================
# REQUIRE ROLES
# Dependency factory: batasi akses berdasarkan role
# =========================================================

def require_roles(*allowed_roles: UserRole):
    """
    Dependency factory untuk membatasi endpoint ke role tertentu.

    Cara kerja:
    - Memanggil get_current_user() terlebih dahulu
    - Mengecek apakah role user termasuk dalam allowed_roles
    - Jika tidak, raise HTTP 403 Forbidden

    Raises:
        403 - Role user tidak memiliki akses ke endpoint ini

    Contoh pemakaian di route:

        # Hanya admin dan laboran
        current_user = Depends(require_roles(UserRole.ADMIN, UserRole.LABORAN))

        # Hanya admin
        current_user = Depends(require_roles(UserRole.ADMIN))

        # Semua role yang login (tidak perlu require_roles, cukup get_current_user)
        current_user = Depends(get_current_user)
    """
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