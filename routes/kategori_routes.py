# app/routes/kategori_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.kategori_alat import (
    KategoriAlatCreate,
    KategoriAlatResponse,
)

from app.services.kategori_service import (
    get_all_kategori,
    get_kategori_by_id,
    create_kategori,
    update_kategori,
    delete_kategori,
)

from app.middleware.auth_middleware import (
    get_current_user,
    require_roles,
)

from app.constants.enums import UserRole


router = APIRouter(
    prefix="/kategori",
    tags=["Kategori"],
)

@router.get(
    "/",
    response_model=list[KategoriAlatResponse],
)
def list_kategori(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_all_kategori(db)

@router.get(
    "/{kategori_id}",
    response_model=KategoriAlatResponse,
)
def detail_kategori(
    kategori_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_kategori_by_id(db, kategori_id)

@router.post(
    "/",
    response_model=KategoriAlatResponse,
)
def add_kategori(
    kategori_data: KategoriAlatCreate,
    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LABORAN,
        )
    ),
):
    return create_kategori(db, kategori_data)

@router.put(
    "/{kategori_id}",
    response_model=KategoriAlatResponse,
)
def edit_kategori(
    kategori_id: int,
    update_data: KategoriAlatCreate,
    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LABORAN,
        )
    ),
):
    return update_kategori(
        db,
        kategori_id,
        update_data,
    )

@router.delete(
    "/{kategori_id}",
)
def remove_kategori(
    kategori_id: int,
    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
):
    return delete_kategori(db, kategori_id)