from sqlalchemy.orm import Session
from app.models.pengembalian import Pengembalian
from app.schemas.pengembalian import PengembalianCreate
from app.models.detail_peminjaman import DetailPeminjaman


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
    new_data = Pengembalian(**data)

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

def update_kondisi_akhir_detail(
    db: Session,
    detail_id: int,
    kondisi_akhir,
    catatan_pengembalian: str = None,
):

    detail = db.query(DetailPeminjaman).filter(
        DetailPeminjaman.id == detail_id
    ).first()

    if not detail:
        return None

    detail.kondisi_akhir = kondisi_akhir
    detail.catatan_pengembalian = catatan_pengembalian

    db.flush()

    return detail

def delete_pengembalian(db: Session, pengembalian_id: int):
    data = get_pengembalian_by_id(db, pengembalian_id)

    if not data:
        return None

    db.delete(data)
    db.commit()

    return data