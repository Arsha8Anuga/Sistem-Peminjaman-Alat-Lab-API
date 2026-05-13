# app/services/upload_service.py

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.utils.file_upload import save_file, delete_file
from app.repositories import user_repository, alat_repository
from app.constants import HttpCode


def upload_file(db: Session, entity_type: str, entity_id: int, file):

    if entity_type not in ["user", "alat"]:
        raise HTTPException(status_code=400, detail="Invalid entity type")

    new_path = save_file(file, folder=entity_type + "s")

    if entity_type == "user":
        entity = user_repository.get_user_by_id(db, entity_id)
    else:
        entity = alat_repository.get_alat_by_id(db, entity_id)

    if not entity:
        delete_file(new_path)
        raise HTTPException(status_code=404, detail="Entity not found")

    old_path = entity.foto

    try:
        # update DB dulu
        if entity_type == "user":
            user_repository.update_user(db, entity_id, {"foto": new_path})
        else:
            alat_repository.update_alat(db, entity_id, {"foto": new_path})

        db.commit()

        # baru hapus file lama
        if old_path:
            delete_file(old_path)

        return {"foto": new_path}

    except Exception:
        db.rollback()
        delete_file(new_path)
        raise