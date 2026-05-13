# app/routes/peminjaman_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.peminjaman import (
    PeminjamanAjukan,
    PeminjamanResponse,
)

from app.services.peminjaman_service import (
    get_all_peminjaman,
    get_peminjaman_by_id,
    ajukan_peminjaman,
    setujui_peminjaman,
    tolak_peminjaman,
    ambil_alat,
    batalkan_peminjaman,
)

from app.middleware.auth_middleware import (
    get_current_user,
    require_roles,
)

from app.constants.enums import UserRole

router = APIRouter(
    prefix="/peminjaman",
    tags=["Peminjaman"],
)


# =========================================================
# LIST PEMINJAMAN
# =========================================================
@router.get(
    "/",
    response_model=list[PeminjamanResponse],
)
def list_peminjaman(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_all_peminjaman(
        db,
        page,
        page_size,
        current_user,
    )


# =========================================================
# DETAIL PEMINJAMAN
# =========================================================
@router.get(
    "/{peminjaman_id}",
    response_model=PeminjamanResponse,
)
def detail_peminjaman(
    peminjaman_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_peminjaman_by_id(
        db,
        peminjaman_id,
        current_user,
    )


# =========================================================
# AJUKAN PEMINJAMAN
# MAHASISWA ONLY
# =========================================================
@router.post(
    "/",
    response_model=PeminjamanResponse,
)
def create_peminjaman(
    data: PeminjamanAjukan,          # ← sebelumnya: data: dict
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.MAHASISWA)
    ),
):
    return ajukan_peminjaman(
        db,
        current_user.id,
        data,                         # ← PeminjamanAjukan diteruskan ke service
    )


# =========================================================
# APPROVE
# LABORAN / ADMIN
# =========================================================
@router.put(
    "/{peminjaman_id}/approve",
    response_model=PeminjamanResponse,
)
def approve(
    peminjaman_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.LABORAN,
            UserRole.ADMIN,
        )
    ),
):
    return setujui_peminjaman(
        db,
        peminjaman_id,
        current_user.id,
    )


# =========================================================
# REJECT
# =========================================================
@router.put(
    "/{peminjaman_id}/reject",
    response_model=PeminjamanResponse,
)
def reject(
    peminjaman_id: int,
    catatan: str = "",
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.LABORAN,
            UserRole.ADMIN,
        )
    ),
):
    return tolak_peminjaman(
        db,
        peminjaman_id,
        catatan,
    )


# =========================================================
# AMBIL ALAT
# =========================================================
@router.put(
    "/{peminjaman_id}/ambil",
    response_model=PeminjamanResponse,
)
def ambil(
    peminjaman_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.LABORAN,
            UserRole.ADMIN,
        )
    ),
):
    return ambil_alat(
        db,
        peminjaman_id,
    )


# =========================================================
# CANCEL
# MAHASISWA SENDIRI
# =========================================================
@router.put(
    "/{peminjaman_id}/cancel",
    response_model=PeminjamanResponse,
)
def cancel(
    peminjaman_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.MAHASISWA)
    ),
):
    return batalkan_peminjaman(
        db,
        peminjaman_id,
        current_user.id,
    )