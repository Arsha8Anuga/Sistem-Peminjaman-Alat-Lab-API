from sqlalchemy.orm import Session
from app.models.pengembalian import Pengembalian
from app.schemas.pengembalian import PengembalianCreate


def get_all_pengembalian(db: Session):
    return db.query(Pengembalian).all()

def get_pengembalian_by_id(db: Session, pengembalian_id: int):
    return db.query(Pengembalian).filter(
        Pengembalian.id == pengembalian_id
    ).first()

def get_pengembalian_by_peminjaman(db: Session, peminjaman_id: int):
    return db.query(Pengembalian).filter(
        Pengembalian.peminjaman_id == peminjaman_id
    ).first()

def create_pengembalian(db: Session, data: PengembalianCreate):
    new_data = Pengembalian(**data.model_dump())

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return new_data

def update_pengembalian(db: Session, pengembalian_id: int, update_data: dict):
    data = get_pengembalian_by_id(db, pengembalian_id)

    if not data:
        return None

    allowed_fields = {
        "tanggal_dikembalikan",
        "denda",
        "status_verifikasi",
        "catatan",
        "diterima_oleh",
    }

    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(data, key, value)

    db.commit()
    db.refresh(data)

    return data

def delete_pengembalian(db: Session, pengembalian_id: int):
    data = get_pengembalian_by_id(db, pengembalian_id)

    if not data:
        return None

    db.delete(data)
    db.commit()

    return data