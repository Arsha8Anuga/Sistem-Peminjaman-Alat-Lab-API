from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.peminjaman import Peminjaman
from app.models.detail_peminjaman import DetailPeminjaman
from app.constants.enums import StatusPeminjaman


def get_all_peminjaman(db: Session, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    return db.query(Peminjaman).offset(skip).limit(page_size).all()


def get_peminjaman_by_id(db: Session, peminjaman_id: int):
    return db.query(Peminjaman).filter(Peminjaman.id == peminjaman_id).first()


def get_peminjaman_by_kode(db: Session, kode_peminjaman: str):
    return (
        db.query(Peminjaman)
        .filter(Peminjaman.kode_peminjaman == kode_peminjaman)
        .first()
    )


def get_peminjaman_by_mahasiswa_id(db: Session, mahasiswa_id: int):
    return (
        db.query(Peminjaman)
        .filter(Peminjaman.mahasiswa_id == mahasiswa_id)
        .order_by(Peminjaman.created_at.desc())
        .all()
    )


def create_peminjaman(db: Session, *args, **kwargs):
    if args and hasattr(args[0], "model_dump"):
        data = args[0].model_dump()
        new_data = Peminjaman(**data)
        db.add(new_data)
        return new_data

    new_data = Peminjaman(
        kode_peminjaman=kwargs["kode_peminjaman"],
        mahasiswa_id=kwargs["mahasiswa_id"],
        tanggal_pengajuan=datetime.now(timezone.utc),
        tanggal_pinjam=kwargs["tanggal_pinjam"],
        tanggal_rencana_kembali=kwargs["tanggal_rencana_kembali"],
        status=StatusPeminjaman.PENDING,
        catatan=kwargs.get("catatan"),
    )
    db.add(new_data)
    db.flush()

    for detail in kwargs.get("detail_list", []):
        db.add(
            DetailPeminjaman(
                peminjaman_id=new_data.id,
                alat_id=detail.alat_id,
                jumlah=detail.jumlah,
            )
        )

    return new_data


def update_peminjaman(db: Session, peminjaman_id: int, update_data: dict):
    peminjaman = get_peminjaman_by_id(db, peminjaman_id)
    if not peminjaman:
        return None

    allowed_fields = {
        "tanggal_pengajuan",
        "tanggal_pinjam",
        "tanggal_rencana_kembali",
        "status",
        "catatan",
        "disetujui_oleh",
    }

    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(peminjaman, key, value)

    return peminjaman


def update_status_peminjaman(
    db: Session,
    peminjaman_id: int,
    status: StatusPeminjaman,
    disetujui_oleh: int | None = None,
    catatan: str | None = None,
):
    update_data = {"status": status}

    if disetujui_oleh is not None:
        update_data["disetujui_oleh"] = disetujui_oleh

    if catatan is not None:
        update_data["catatan"] = catatan

    return update_peminjaman(db, peminjaman_id, update_data)


def delete_peminjaman(db: Session, peminjaman_id: int):
    peminjaman = get_peminjaman_by_id(db, peminjaman_id)
    if not peminjaman:
        return None

    db.delete(peminjaman)
    return peminjaman
