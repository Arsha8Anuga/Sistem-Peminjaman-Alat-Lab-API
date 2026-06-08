# app/repositories/peminjaman_repository.py

from sqlalchemy.orm import Session

from app.models.peminjaman import Peminjaman
from app.schemas.peminjaman import PeminjamanCreate

def get_all_peminjaman(db: Session):
    return db.query(Peminjaman).all()


def get_all_peminjaman_paginated(db: Session, page: int, page_size: int):
    """
    Mengambil semua peminjaman dengan pagination.
    Digunakan oleh admin / laboran / asisten.
    """
    offset = (page - 1) * page_size
    return (
        db.query(Peminjaman)
        .offset(offset)
        .limit(page_size)
        .all()
    )


def get_peminjaman_by_mahasiswa_id(
    db: Session,
    mahasiswa_id: int,
    page: int,
    page_size: int,
):

    offset = (page - 1) * page_size
    return (
        db.query(Peminjaman)
        .filter(Peminjaman.mahasiswa_id == mahasiswa_id)
        .offset(offset)
        .limit(page_size)
        .all()
    )


def get_peminjaman_by_id(db: Session, peminjaman_id: int):
    return (
        db.query(Peminjaman)
        .filter(Peminjaman.id == peminjaman_id)
        .first()
    )


def get_peminjaman_by_kode(db: Session, kode_peminjaman: str):
    return (
        db.query(Peminjaman)
        .filter(Peminjaman.kode_peminjaman == kode_peminjaman)
        .first()
    )

def create_peminjaman(db: Session, data: PeminjamanCreate):
    new_data = Peminjaman(**data)
    db.commit()
    db.refresh(new_data)
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

    db.commit()
    db.refresh(peminjaman)
    return peminjaman

def delete_peminjaman(db: Session, peminjaman_id: int):
    peminjaman = get_peminjaman_by_id(db, peminjaman_id)
    if not peminjaman:
        return None
    db.delete(peminjaman)
    db.commit()
    return peminjaman

def update_status_peminjaman(
    db: Session,
    peminjaman_id: int,
    status,
):

    peminjaman = get_peminjaman_by_id(
        db,
        peminjaman_id,
    )

    if not peminjaman:
        return None

    peminjaman.status = status

    db.add(peminjaman)

    return peminjaman