from sqlalchemy.orm import Session

from app.models.alat import Alat
from app.models.kondisi_log import KondisiLog

from app.schemas.alat import AlatCreate

from app.constants.enums import KondisiFisik

def get_all_alat(
    db: Session,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Alat)
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_alat(db: Session):
    return db.query(Alat).count()


def get_alat_by_id(db: Session, alat_id: int):
    return db.query(Alat).filter(
        Alat.id == alat_id
    ).first()


def get_alat_by_kode(db: Session, kode_alat: str):
    return db.query(Alat).filter(
        Alat.kode_alat == kode_alat
    ).first()

def create_alat(
    db: Session,
    alat_data: dict
):

    new_alat = Alat(**alat_data)

    db.add(new_alat)
    db.commit()
    db.refresh(new_alat)

    return new_alat

def update_alat(
    db: Session,
    alat_id: int,
    update_data: dict
):

    alat = get_alat_by_id(db, alat_id)

    if not alat:
        return None

    for key, value in update_data.items():
        setattr(alat, key, value)

    db.commit()
    db.refresh(alat)

    return alat

def delete_alat(
    db: Session,
    alat_id: int
):

    alat = get_alat_by_id(db, alat_id)

    if not alat:
        return None

    db.delete(alat)
    db.commit()

    return alat

def tambah_stok(
    db: Session,
    alat_id: int,
    jumlah: int,
):

    alat = get_alat_by_id(db, alat_id)

    if not alat:
        return None

    alat.stok_tersedia += jumlah

    db.flush()

    return alat


def kurangi_stok_total(
    db: Session,
    alat_id: int,
    jumlah: int,
):

    alat = get_alat_by_id(db, alat_id)

    if not alat:
        return None

    alat.stok_total -= jumlah

    if alat.stok_total < 0:
        alat.stok_total = 0

    db.flush()

    return alat

def update_kondisi_fisik(
    db: Session,
    alat_id: int,
    kondisi: KondisiFisik,
):

    alat = get_alat_by_id(db, alat_id)

    if not alat:
        return None

    alat.kondisi_fisik = kondisi

    db.flush()

    return alat

def catat_kondisi_log(
    db: Session,
    alat_id: int,
    peminjaman_id: int,
    kondisi,
    catatan_kerusakan: str,
    dicatat_oleh: int,
):

    new_log = KondisiLog(
        alat_id=alat_id,
        peminjaman_id=peminjaman_id,
        kondisi=kondisi,
        catatan_kerusakan=catatan_kerusakan,
        dicatat_oleh=dicatat_oleh,
    )

    db.add(new_log)

    return new_log