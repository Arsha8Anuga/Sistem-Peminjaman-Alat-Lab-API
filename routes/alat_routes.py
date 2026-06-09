from fastapi import APIRouter, Depends
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

router = APIRouter(prefix="/alat", tags=["Alat"])


@router.get("/")
def list_alat(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
):
    data, total = get_all_alat(db, page, page_size)
    return {
        "data": data,
        "meta": {
            "page": page,
            "page_size": page_size,
            "total": total,
        },
    }


@router.get("/{alat_id}", response_model=AlatResponse)
def detail_alat(alat_id: int, db: Session = Depends(get_db)):
    return get_alat_by_id(db, alat_id)


@router.post("/", response_model=AlatResponse)
def add_alat(
    alat_data: AlatCreate,
    db: Session = Depends(get_db),
):
    return create_alat(db, alat_data)


@router.put("/{alat_id}", response_model=AlatResponse)
def edit_alat(
    alat_id: int,
    update_data: AlatUpdate,
    db: Session = Depends(get_db),
):
    return update_alat(db, alat_id, update_data)


@router.delete("/{alat_id}")
def remove_alat(alat_id: int, db: Session = Depends(get_db)):
    return delete_alat(db, alat_id)
