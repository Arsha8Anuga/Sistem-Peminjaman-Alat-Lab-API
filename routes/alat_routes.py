from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.alat import AlatCreate, AlatUpdate
from app.services.alat_service import (
    get_all_alat,
    get_alat_by_id,
    create_alat,
    update_alat,
    delete_alat,
)

router = APIRouter(prefix="/alat", tags=["Alat"])


# ======================
# LIST
# ======================
@router.get("/")
def list_alat(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    return get_all_alat(db, page, page_size)


# ======================
# DETAIL
# ======================
@router.get("/{alat_id}")
def detail_alat(alat_id: int, db: Session = Depends(get_db)):
    return get_alat_by_id(db, alat_id)


# ======================
# CREATE + IMAGE UPLOAD
# ======================
@router.post("/")
def add_alat(
    alat_data: AlatCreate = Depends(),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    return create_alat(db, alat_data, file)


# ======================
# UPDATE + IMAGE UPLOAD
# ======================
@router.put("/{alat_id}")
def edit_alat(
    alat_id: int,
    update_data: AlatUpdate = Depends(),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    return update_alat(db, alat_id, update_data, file)


# ======================
# DELETE
# ======================
@router.delete("/{alat_id}")
def remove_alat(alat_id: int, db: Session = Depends(get_db)):
    return delete_alat(db, alat_id)