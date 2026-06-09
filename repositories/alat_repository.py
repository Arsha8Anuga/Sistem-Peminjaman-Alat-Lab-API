from sqlalchemy.orm import Session

from app.models.alat import Alat
from app.models.kondisi_log import KondisiLog
from app.constants.enums import StatusKetersediaan


def _sync_status_ketersediaan(alat: Alat):
    if alat.stok_tersedia <= 0:
        alat.status_ketersediaan = StatusKetersediaan.DIPINJAM
    elif alat.status_ketersediaan == StatusKetersediaan.DIPINJAM:
        alat.status_ketersediaan = StatusKetersediaan.TERSEDIA


def get_all_alat(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Alat).offset(skip).limit(limit).all()


def count_alat(db: Session):
    return db.query(Alat).count()


def get_alat_by_id(db: Session, alat_id: int):
    return db.query(Alat).filter(Alat.id == alat_id).first()


def get_alat_by_kode(db: Session, kode_alat: str):
    return db.query(Alat).filter(Alat.kode_alat == kode_alat).first()


def create_alat(db: Session, alat_data):
    if hasattr(alat_data, "model_dump"):
        alat_data = alat_data.model_dump()

    new_alat = Alat(**alat_data)
    _sync_status_ketersediaan(new_alat)
    db.add(new_alat)
    return new_alat


def update_alat(db: Session, alat_id: int, update_data: dict):
    alat = get_alat_by_id(db, alat_id)
    if not alat:
        return None

    allowed_fields = {
        "kategori_id",
        "kode_alat",
        "nama_alat",
        "merk",
        "spesifikasi",
        "lokasi_penyimpanan",
        "stok_total",
        "stok_tersedia",
        "kondisi_fisik",
        "status_ketersediaan",
        "foto",
        "deskripsi",
    }

    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(alat, key, value)

    _sync_status_ketersediaan(alat)
    return alat


def delete_alat(db: Session, alat_id: int):
    alat = get_alat_by_id(db, alat_id)
    if not alat:
        return None

    db.delete(alat)
    return alat


def kurangi_stok(db: Session, alat_id: int, jumlah: int):
    alat = get_alat_by_id(db, alat_id)
    if not alat:
        return None

    alat.stok_tersedia -= jumlah
    if alat.stok_tersedia < 0:
        alat.stok_tersedia = 0

    _sync_status_ketersediaan(alat)
    return alat


def tambah_stok(db: Session, alat_id: int, jumlah: int):
    alat = get_alat_by_id(db, alat_id)
    if not alat:
        return None

    alat.stok_tersedia += jumlah
    if alat.stok_tersedia > alat.stok_total:
        alat.stok_tersedia = alat.stok_total

    _sync_status_ketersediaan(alat)
    return alat


def kurangi_stok_total(db: Session, alat_id: int, jumlah: int):
    alat = get_alat_by_id(db, alat_id)
    if not alat:
        return None

    alat.stok_total -= jumlah
    if alat.stok_total < 0:
        alat.stok_total = 0

    if alat.stok_tersedia > alat.stok_total:
        alat.stok_tersedia = alat.stok_total

    _sync_status_ketersediaan(alat)
    return alat


def update_kondisi_fisik(db: Session, alat_id: int, kondisi):
    alat = get_alat_by_id(db, alat_id)
    if not alat:
        return None

    alat.kondisi_fisik = kondisi
    return alat


def catat_kondisi_log(
    db: Session,
    alat_id: int,
    peminjaman_id: int,
    kondisi,
    catatan: str | None,
    dicatat_oleh: int,
):
    log = KondisiLog(
        alat_id=alat_id,
        peminjaman_id=peminjaman_id,
        kondisi=kondisi,
        catatan_kerusakan=catatan,
        dicatat_oleh=dicatat_oleh,
    )
    db.add(log)
    return log
