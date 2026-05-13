# app/services/peminjaman_service.py

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import peminjaman_repository
from app.schemas.peminjaman import PeminjamanAjukan, PeminjamanCreate
from app.constants.enums import UserRole, StatusPeminjaman


# =========================================================
# HELPER
# =========================================================

def _generate_kode() -> str:
    tanggal = datetime.now(timezone.utc).strftime("%Y%m%d")
    suffix = uuid.uuid4().hex[:4].upper()
    return f"PJM-{tanggal}-{suffix}"


def _get_or_404(db: Session, peminjaman_id: int):
    data = peminjaman_repository.get_peminjaman_by_id(db, peminjaman_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Peminjaman tidak ditemukan",
        )
    return data


# =========================================================
# GET ALL
# Mahasiswa  → hanya lihat miliknya sendiri
# Selain itu → lihat semua
# =========================================================

def get_all_peminjaman(
    db: Session,
    page: int,
    page_size: int,
    current_user,
):
    if current_user.role == UserRole.MAHASISWA:
        # Filter hanya peminjaman milik mahasiswa yang login
        return peminjaman_repository.get_peminjaman_by_mahasiswa_id(
            db,
            mahasiswa_id=current_user.id,
            page=page,
            page_size=page_size,
        )

    # Admin / laboran / asisten → semua data
    return peminjaman_repository.get_all_peminjaman_paginated(
        db,
        page=page,
        page_size=page_size,
    )


# =========================================================
# GET BY ID
# Mahasiswa  → hanya boleh lihat punyanya sendiri (403 jika bukan)
# Selain itu → boleh lihat siapa saja
# =========================================================

def get_peminjaman_by_id(
    db: Session,
    peminjaman_id: int,
    current_user,
):
    peminjaman = _get_or_404(db, peminjaman_id)

    if (
        current_user.role == UserRole.MAHASISWA
        and peminjaman.mahasiswa_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses ke peminjaman ini",
        )

    return peminjaman


# =========================================================
# AJUKAN PEMINJAMAN (mahasiswa)
# =========================================================

def ajukan_peminjaman(
    db: Session,
    mahasiswa_id: int,
    data: PeminjamanAjukan,
):
    payload = PeminjamanCreate(
        kode_peminjaman=_generate_kode(),
        mahasiswa_id=mahasiswa_id,
        disetujui_oleh=None,
        tanggal_pengajuan=datetime.now(timezone.utc),
        tanggal_pinjam=data.tanggal_pinjam,
        tanggal_rencana_kembali=data.tanggal_rencana_kembali,
        status=StatusPeminjaman.PENDING,
        catatan=data.catatan,
    )
    return peminjaman_repository.create_peminjaman(db, payload)


# =========================================================
# SETUJUI (laboran / admin)
# =========================================================

def setujui_peminjaman(
    db: Session,
    peminjaman_id: int,
    laboran_id: int,
):
    peminjaman = _get_or_404(db, peminjaman_id)

    if peminjaman.status != StatusPeminjaman.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hanya peminjaman berstatus 'pending' yang dapat disetujui",
        )

    return peminjaman_repository.update_peminjaman(
        db,
        peminjaman_id,
        {
            "status": StatusPeminjaman.DISETUJUI,
            "disetujui_oleh": laboran_id,
        },
    )


# =========================================================
# TOLAK (laboran / admin)
# =========================================================

def tolak_peminjaman(
    db: Session,
    peminjaman_id: int,
    catatan: str = "",
):
    peminjaman = _get_or_404(db, peminjaman_id)

    if peminjaman.status != StatusPeminjaman.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hanya peminjaman berstatus 'pending' yang dapat ditolak",
        )

    return peminjaman_repository.update_peminjaman(
        db,
        peminjaman_id,
        {
            "status": StatusPeminjaman.DITOLAK,
            "catatan": catatan,
        },
    )


# =========================================================
# AMBIL ALAT — konfirmasi alat sudah diambil (laboran / admin)
# =========================================================

def ambil_alat(db: Session, peminjaman_id: int):
    peminjaman = _get_or_404(db, peminjaman_id)

    if peminjaman.status != StatusPeminjaman.DISETUJUI:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hanya peminjaman berstatus 'disetujui' yang dapat dikonfirmasi pengambilan",
        )

    return peminjaman_repository.update_peminjaman(
        db,
        peminjaman_id,
        {"status": StatusPeminjaman.DIPINJAM},
    )


# =========================================================
# BATALKAN (mahasiswa — hanya miliknya sendiri)
# =========================================================

def batalkan_peminjaman(
    db: Session,
    peminjaman_id: int,
    mahasiswa_id: int,
):
    peminjaman = _get_or_404(db, peminjaman_id)

    # Pastikan ini memang peminjaman milik mahasiswa yang request
    if peminjaman.mahasiswa_id != mahasiswa_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses ke peminjaman ini",
        )

    if peminjaman.status != StatusPeminjaman.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hanya peminjaman berstatus 'pending' yang dapat dibatalkan",
        )

    return peminjaman_repository.update_peminjaman(
        db,
        peminjaman_id,
        {"status": StatusPeminjaman.DIBATALKAN},
    )