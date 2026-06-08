from sqlalchemy.orm import Session
from app.models.kategori_alat import KategoriAlat
from app.schemas.kategori_alat import KategoriAlatCreate

def get_all_kategori(db: Session):
    return db.query(KategoriAlat).all()


def get_kategori_by_id(db: Session, kategori_id: int):
    return (
        db.query(KategoriAlat)
        .filter(KategoriAlat.id == kategori_id)
        .first()
    )


def get_kategori_by_nama(db: Session, nama_kategori: str):
    return (
        db.query(KategoriAlat)
        .filter(KategoriAlat.nama_kategori == nama_kategori)
        .first()
    )

def create_kategori(db: Session, kategori_data: KategoriAlatCreate):
    new_kategori = KategoriAlat(
        nama_kategori=kategori_data.nama_kategori,
        deskripsi=kategori_data.deskripsi,
    )

    db.add(new_kategori)
    db.commit()
    db.refresh(new_kategori)

    return new_kategori

def update_kategori(db: Session, kategori_id: int, update_data: dict):
    kategori = get_kategori_by_id(db, kategori_id)

    if not kategori:
        return None

    allowed_fields = {
        "nama_kategori",
        "deskripsi",
    }

    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(kategori, key, value)

    db.commit()
    db.refresh(kategori)

    return kategori

def delete_kategori(db: Session, kategori_id: int):
    kategori = get_kategori_by_id(db, kategori_id)

    if not kategori:
        return None

    db.delete(kategori)
    db.commit()

    return kategori

def count_kategori(db: Session):
    return db.query(KategoriAlat).count()