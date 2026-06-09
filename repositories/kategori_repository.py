from sqlalchemy.orm import Session
from app.models.kategori_alat import KategoriAlat


def get_all_kategori(db: Session):
    return db.query(KategoriAlat).all()


def get_kategori_by_id(db: Session, kategori_id: int):
    return db.query(KategoriAlat).filter(KategoriAlat.id == kategori_id).first()


def get_kategori_by_nama(db: Session, nama_kategori: str):
    return (
        db.query(KategoriAlat)
        .filter(KategoriAlat.nama_kategori == nama_kategori)
        .first()
    )


def create_kategori(db: Session, kategori_data):
    if hasattr(kategori_data, "model_dump"):
        kategori_data = kategori_data.model_dump()

    new_kategori = KategoriAlat(**kategori_data)
    db.add(new_kategori)
    return new_kategori


def update_kategori(db: Session, kategori_id: int, update_data: dict):
    kategori = get_kategori_by_id(db, kategori_id)
    if not kategori:
        return None

    if hasattr(update_data, "model_dump"):
        update_data = update_data.model_dump(exclude_unset=True)

    allowed_fields = {"nama_kategori", "deskripsi"}
    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(kategori, key, value)

    return kategori


def delete_kategori(db: Session, kategori_id: int):
    kategori = get_kategori_by_id(db, kategori_id)
    if not kategori:
        return None

    db.delete(kategori)
    return kategori


def count_kategori(db: Session):
    return db.query(KategoriAlat).count()
