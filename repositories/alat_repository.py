from sqlalchemy.orm import Session
from app.models.alat import Alat
from app.schemas.alat import AlatCreate


def get_all_alat(db: Session):
    return db.query(Alat).all()

def get_alat_by_id(db: Session, alat_id: int):
    return db.query(Alat).filter(Alat.id == alat_id).first()

def get_alat_by_kode(db: Session, kode_alat: str):
    return db.query(Alat).filter(Alat.kode_alat == kode_alat).first()

def create_alat(db: Session, alat_data: AlatCreate):
    new_alat = Alat(**alat_data.model_dump())
    db.add(new_alat)
    return new_alat


def update_alat(db: Session, alat_id: int, update_data: dict):
    alat = get_alat_by_id(db, alat_id)

    if not alat:
        return None

    for key, value in update_data.items():
        setattr(alat, key, value)

    return alat


def delete_alat(db: Session, alat_id: int):
    alat = get_alat_by_id(db, alat_id)

    if not alat:
        return None

    db.delete(alat)
    return alat