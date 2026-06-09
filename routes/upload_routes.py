from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.upload_service import upload_file

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post(
    "/user/{user_id}",
    operation_id="upload_user_photo_v1",
)
def upload_user_photo(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return upload_file(db, "user", user_id, file)


@router.post(
    "/alat/{alat_id}",
    operation_id="upload_alat_photo_v1",
)
def upload_alat_photo(
    alat_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return upload_file(db, "alat", alat_id, file)


@router.post(
    "/{entity_type}/{entity_id}",
    operation_id="upload_generic_v1",
)
def upload_generic(
    entity_type: str,
    entity_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return upload_file(db, entity_type, entity_id, file)
