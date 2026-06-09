from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import kategori_repository
from app.constants import HttpCode, ResponseMessage


def get_all_kategori(db: Session):
    return kategori_repository.get_all_kategori(db)


def get_kategori_by_id(db: Session, kategori_id: int):
    kategori = kategori_repository.get_kategori_by_id(db, kategori_id)
    if not kategori:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.KATEGORI_NOT_FOUND,
        )
    return kategori


def create_kategori(db: Session, kategori_data):
    try:
        existing = kategori_repository.get_kategori_by_nama(
            db, kategori_data.nama_kategori
        )
        if existing:
            raise HTTPException(
                status_code=HttpCode.CONFLICT,
                detail="Nama kategori sudah digunakan",
            )

        new_kategori = kategori_repository.create_kategori(db, kategori_data)
        db.commit()
        db.refresh(new_kategori)
        return new_kategori

    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=HttpCode.CONFLICT,
            detail="Nama kategori sudah digunakan",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HttpCode.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


def update_kategori(db: Session, kategori_id: int, update_data):
    try:
        kategori = get_kategori_by_id(db, kategori_id)
        data = update_data.model_dump(exclude_unset=True)

        if "nama_kategori" in data and data["nama_kategori"] != kategori.nama_kategori:
            existing = kategori_repository.get_kategori_by_nama(
                db, data["nama_kategori"]
            )
            if existing:
                raise HTTPException(
                    status_code=HttpCode.CONFLICT,
                    detail="Nama kategori sudah digunakan",
                )

        updated = kategori_repository.update_kategori(db, kategori_id, data)
        db.commit()
        db.refresh(updated)
        return updated

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HttpCode.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


def delete_kategori(db: Session, kategori_id: int):
    try:
        get_kategori_by_id(db, kategori_id)
        deleted = kategori_repository.delete_kategori(db, kategori_id)
        db.commit()
        return deleted

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HttpCode.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
