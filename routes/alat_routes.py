# app/routes/alat_routes.py

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.alat import AlatCreate, AlatUpdate, AlatResponse

from app.services.alat_service import (
    get_all_alat,
    get_alat_by_id,
    create_alat,
    update_alat,
    delete_alat,
)

from app.middleware.auth_middleware import (
    get_current_user,
    require_roles,
)

from app.constants.enums import UserRole

router = APIRouter(prefix="/alat", tags=["Alat"])


# ======================
# LIST
# Semua user yang login boleh lihat daftar alat
# ======================
@router.get(
    "/",
    response_model=list[AlatResponse],
)
def list_alat(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),         # ← login required
):
    return get_all_alat(db, page, page_size)


# ======================
# DETAIL
# Semua user yang login boleh lihat detail alat
# ======================
@router.get(
    "/{alat_id}",
    response_model=AlatResponse,
)
def detail_alat(
    alat_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),         # ← login required
):
    return get_alat_by_id(db, alat_id)


# ======================
# CREATE + IMAGE UPLOAD
# Hanya admin dan laboran
# ======================
@router.post(
    "/",
    response_model=AlatResponse,
)
def add_alat(
    alat_data: AlatCreate = Depends(),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(                           # ← admin / laboran only
        require_roles(
            UserRole.ADMIN,
            UserRole.LABORAN,
        )
    ),
):
    return create_alat(db, alat_data, file)


# ======================
# UPDATE + IMAGE UPLOAD
# Hanya admin dan laboran
# ======================
@router.put(
    "/{alat_id}",
    response_model=AlatResponse,
)
def edit_alat(
    alat_id: int,
    update_data: AlatUpdate = Depends(),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(                           # ← admin / laboran only
        require_roles(
            UserRole.ADMIN,
            UserRole.LABORAN,
        )
    ),
):
    return update_alat(db, alat_id, update_data, file)


# ======================
# DELETE
# Hanya admin
# ======================
@router.delete(
    "/{alat_id}",
)
def remove_alat(
    alat_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(                           # ← admin only
        require_roles(UserRole.ADMIN)
    ),
):
    return delete_alat(db, alat_id)