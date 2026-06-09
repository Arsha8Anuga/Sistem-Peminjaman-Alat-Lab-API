from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.pengembalian import (
    PengembalianCreate,
    PengembalianVerify,
    PengembalianResponse,
)
from app.services.pengembalian_service import (
    get_pengembalian_by_peminjaman,
    catat_pengembalian,
    verifikasi_pengembalian,
)
from app.middleware.auth_middleware import get_current_user, require_roles
from app.constants.enums import UserRole

router = APIRouter(
    prefix="/pengembalian",
    tags=["Pengembalian"],
)


@router.get(
    "/{peminjaman_id}",
    response_model=PengembalianResponse,
)
def detail_pengembalian(
    peminjaman_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_pengembalian_by_peminjaman(db, peminjaman_id)


@router.post(
    "/",
    response_model=PengembalianResponse,
)
def create_pengembalian(
    data: PengembalianCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LABORAN,
            UserRole.ASISTEN,
        )
    ),
):
    return catat_pengembalian(
        db,
        peminjaman_id=data.peminjaman_id,
        diterima_oleh=current_user.id,
        pengembalian_data=data,
    )


@router.put(
    "/{pengembalian_id}/verify",
    response_model=PengembalianResponse,
)
def verify(
    pengembalian_id: int,
    data: PengembalianVerify,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LABORAN,
        )
    ),
):
    return verifikasi_pengembalian(
        db,
        pengembalian_id,
        data,
    )
