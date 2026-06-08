from sqlalchemy.orm import Session
from app.repositories import alat_repository
from app.models.alat import Alat
from app.constants import HttpCode, ResponseMessage
from app.utils.file_upload import save_file, delete_file, is_valid_image
from fastapi import HTTPException, UploadFile

def get_all_alat(
    db: Session,
    page: int = 1,
    page_size: int = 10
):

    skip = (page - 1) * page_size

    data = alat_repository.get_all_alat(
        db,
        skip=skip,
        limit=page_size
    )

    return data

def get_alat_by_id(
    db: Session,
    alat_id: int
) -> Alat:

    alat = alat_repository.get_alat_by_id(
        db,
        alat_id
    )

    if not alat:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.ALAT_NOT_FOUND,
        )

    return alat

def create_alat(
    db: Session,
    alat_data,
    file: UploadFile = None
):

    try:

        if alat_data.stok_total < 0 or alat_data.stok_tersedia < 0:
            raise HTTPException(
                status_code=HttpCode.BAD_REQUEST,
                detail="Stok tidak boleh bernilai negatif.",
            )

        if alat_data.stok_tersedia > alat_data.stok_total:
            raise HTTPException(
                status_code=HttpCode.BAD_REQUEST,
                detail="Stok tersedia tidak boleh melebihi stok total.",
            )

        data = alat_data.model_dump()

        if file:

            if not is_valid_image(file):
                raise HTTPException(
                    status_code=HttpCode.BAD_REQUEST,
                    detail="File harus gambar (jpg, jpeg, png, webp).",
                )

            path = save_file(file, "alat")

            data["foto"] = path

        new_alat = alat_repository.create_alat(
            db,
            data
        )

        return new_alat

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def update_alat(
    db: Session,
    alat_id: int,
    update_data,
    file=None
):

    alat = alat_repository.get_alat_by_id(
        db,
        alat_id
    )

    if not alat:
        raise HTTPException(
            HttpCode.NOT_FOUND,
            ResponseMessage.ALAT_NOT_FOUND
        )

    try:

        data = update_data.model_dump(
            exclude_unset=True
        )

        if file:

            if not is_valid_image(file):
                raise HTTPException(
                    status_code=HttpCode.BAD_REQUEST,
                    detail="File harus gambar (jpg, jpeg, png, webp).",
                )

            if alat.foto:
                delete_file(alat.foto)

            path = save_file(file, "alat")

            data["foto"] = path

        updated = alat_repository.update_alat(
            db,
            alat_id,
            data
        )

        return updated

    except Exception:
        db.rollback()
        raise

def delete_alat(
    db: Session,
    alat_id: int
):

    alat = alat_repository.get_alat_by_id(
        db,
        alat_id
    )

    if not alat:
        raise HTTPException(
            HttpCode.NOT_FOUND,
            ResponseMessage.ALAT_NOT_FOUND
        )

    try:

        if alat.foto:
            delete_file(alat.foto)

        deleted = alat_repository.delete_alat(
            db,
            alat_id
        )

        return deleted

    except Exception:
        db.rollback()
        raise