from sqlalchemy.orm import Session

from app.models.pengembalian import Pengembalian
from app.models.detail_peminjaman import DetailPeminjaman


def get_all_pengembalian(db: Session):
    return db.query(Pengembalian).all()


def get_pengembalian_by_id(db: Session, pengembalian_id: int):
    return db.query(Pengembalian).filter(Pengembalian.id == pengembalian_id).first()


def get_pengembalian_by_peminjaman(db: Session, peminjaman_id: int):
    return (
        db.query(Pengembalian)
        .filter(Pengembalian.peminjaman_id == peminjaman_id)
        .first()
    )


def get_pengembalian_by_peminjaman_id(db: Session, peminjaman_id: int):
    return get_pengembalian_by_peminjaman(db, peminjaman_id)


def create_pengembalian(db: Session, *args, **kwargs):
    if args and hasattr(args[0], "model_dump"):
        data = args[0].model_dump(exclude={"detail"})
        new_data = Pengembalian(**data)
    else:
        new_data = Pengembalian(**kwargs)

    db.add(new_data)
    db.flush()
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

    return data


def update_status_verifikasi(
    db: Session,
    pengembalian_id: int,
    status_verifikasi,
    catatan: str | None = None,
):
    return update_pengembalian(
        db,
        pengembalian_id,
        {
            "status_verifikasi": status_verifikasi,
            "catatan": catatan,
        },
    )


def update_kondisi_akhir_detail(
    db: Session,
    detail_id: int,
    kondisi_akhir,
    catatan_pengembalian: str | None = None,
):
    detail = db.query(DetailPeminjaman).filter(DetailPeminjaman.id == detail_id).first()
    if not detail:
        return None

    detail.kondisi_akhir = kondisi_akhir
    detail.catatan_pengembalian = catatan_pengembalian
    return detail


def delete_pengembalian(db: Session, pengembalian_id: int):
    data = get_pengembalian_by_id(db, pengembalian_id)
    if not data:
        return None

    db.delete(data)
    return data
