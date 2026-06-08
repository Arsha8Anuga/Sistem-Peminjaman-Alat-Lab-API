# app/services/kategori_service.py

from fastapi import HTTPException
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
        new_kategori = kategori_repository.create_kategori(db, kategori_data)

        db.commit()
        db.refresh(new_kategori)

        return new_kategori

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HttpCode.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

def update_kategori(db: Session, kategori_id: int, update_data: dict):

    try:
        kategori = get_kategori_by_id(db, kategori_id)

        updated = kategori_repository.update_kategori(db, kategori_id, update_data)

        if not updated:
            raise HTTPException(
                status_code=HttpCode.NOT_FOUND,
                detail=ResponseMessage.KATEGORI_NOT_FOUND,
            )

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
        kategori = get_kategori_by_id(db, kategori_id)

        deleted = kategori_repository.delete_kategori(db, kategori_id)

        if not deleted:
            raise HTTPException(
                status_code=HttpCode.NOT_FOUND,
                detail=ResponseMessage.KATEGORI_NOT_FOUND,
            )

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