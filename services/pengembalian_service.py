# app/services/pengembalian_service.py

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import (
    pengembalian_repository,
    peminjaman_repository,
    alat_repository,
)

from app.middleware.auth_middleware import (
    can_access_peminjaman,
)

from app.constants import (
    HttpCode,
    ResponseMessage,
)

from app.constants.enums import (
    StatusPeminjaman,
    StatusVerifikasiPengembalian,
    KondisiFisik,
)

def _get_peminjaman_or_404(
    db: Session,
    peminjaman_id: int,
):

    peminjaman = peminjaman_repository.get_peminjaman_by_id(
        db,
        peminjaman_id,
    )

    if not peminjaman:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.PEMINJAMAN_NOT_FOUND,
        )

    return peminjaman

def get_pengembalian_by_peminjaman(
    db: Session,
    peminjaman_id: int,
    current_user,
):

    data = pengembalian_repository.get_pengembalian_by_peminjaman(
        db,
        peminjaman_id,
    )

    if not data:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.PENGEMBALIAN_NOT_FOUND,
        )

    can_access_peminjaman(
        data.peminjaman,
        current_user,
    )

    return data

def catat_pengembalian(
    db: Session,
    pengembalian_data,
    current_user,
):

    peminjaman = _get_peminjaman_or_404(
        db,
        pengembalian_data.peminjaman_id,
    )

    if peminjaman.mahasiswa_id != current_user.id:

        raise HTTPException(
            status_code=HttpCode.FORBIDDEN,
            detail=ResponseMessage.FORBIDDEN,
        )

    if peminjaman.status != StatusPeminjaman.DIPINJAM:

        raise HTTPException(
            status_code=HttpCode.BAD_REQUEST,
            detail=ResponseMessage.PEMINJAMAN_INVALID_STATUS,
        )

    existing = pengembalian_repository.get_pengembalian_by_peminjaman(
        db,
        peminjaman.id,
    )

    if existing:

        raise HTTPException(
            status_code=HttpCode.BAD_REQUEST,
            detail="Pengembalian sudah pernah diajukan",
        )

    try:

        pengembalian = pengembalian_repository.create_pengembalian(
            db,
            {
                "peminjaman_id": peminjaman.id,
                "diterima_oleh": None,
                "tanggal_dikembalikan": datetime.now(timezone.utc),
                "denda": pengembalian_data.denda,
                "status_verifikasi": StatusVerifikasiPengembalian.MENUNGGU,
                "catatan": pengembalian_data.catatan,
            }
        )

        for detail in pengembalian_data.detail:

            pengembalian_repository.update_kondisi_akhir_detail(
                db,
                detail_id=detail.detail_peminjaman_id,
                kondisi_akhir=detail.kondisi_akhir,
                catatan_pengembalian=detail.catatan_pengembalian,
            )

            alat_repository.tambah_stok(
                db,
                alat_id=detail.alat_id,
                jumlah=detail.jumlah,
            )

            alat_repository.catat_kondisi_log(
                db,
                alat_id=detail.alat_id,
                peminjaman_id=peminjaman.id,
                kondisi=detail.kondisi_akhir,
                catatan_kerusakan=detail.catatan_pengembalian,
                dicatat_oleh=current_user.id,
            )

            _update_kondisi_fisik_alat_jika_perlu(
                db,
                detail.alat_id,
                detail.kondisi_akhir,
            )

        peminjaman_repository.update_status_peminjaman(
            db,
            peminjaman.id,
            StatusPeminjaman.DIKEMBALIKAN,
        )

        db.commit()
        db.refresh(pengembalian)

        return pengembalian

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

def verifikasi_pengembalian(
    db: Session,
    pengembalian_id: int,
    data,
    current_user,
):

    pengembalian = pengembalian_repository.get_pengembalian_by_id(
        db,
        pengembalian_id,
    )

    if not pengembalian:

        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.PENGEMBALIAN_NOT_FOUND,
        )

    if (
        pengembalian.status_verifikasi
        != StatusVerifikasiPengembalian.MENUNGGU
    ):

        raise HTTPException(
            status_code=HttpCode.BAD_REQUEST,
            detail="Pengembalian sudah diverifikasi",
        )

    try:

        updated = pengembalian_repository.update_pengembalian(
            db,
            pengembalian_id,
            {
                "status_verifikasi": data.status_verifikasi,
                "catatan": data.catatan,
                "diterima_oleh": current_user.id,
            }
        )

        if (
            data.status_verifikasi
            == StatusVerifikasiPengembalian.SESUAI
        ):

            peminjaman_repository.update_status_peminjaman(
                db,
                pengembalian.peminjaman_id,
                StatusPeminjaman.SELESAI,
            )

        elif (
            data.status_verifikasi
            == StatusVerifikasiPengembalian.RUSAK
        ):

            peminjaman_repository.update_status_peminjaman(
                db,
                pengembalian.peminjaman_id,
                StatusPeminjaman.SELESAI,
            )

        elif (
            data.status_verifikasi
            == StatusVerifikasiPengembalian.HILANG
        ):

            peminjaman_repository.update_status_peminjaman(
                db,
                pengembalian.peminjaman_id,
                StatusPeminjaman.SELESAI,
            )

        db.commit()
        db.refresh(updated)

        return updated

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

_URUTAN_KONDISI = [
    KondisiFisik.BAIK,
    KondisiFisik.RUSAK_RINGAN,
    KondisiFisik.RUSAK_BERAT,
    KondisiFisik.MAINTENANCE,
    KondisiFisik.HILANG,
]


def _update_kondisi_fisik_alat_jika_perlu(
    db: Session,
    alat_id: int,
    kondisi_akhir: KondisiFisik,
):

    alat = alat_repository.get_alat_by_id(
        db,
        alat_id,
    )

    if not alat:
        return

    try:

        idx_now = _URUTAN_KONDISI.index(
            alat.kondisi_fisik
        )

        idx_new = _URUTAN_KONDISI.index(
            kondisi_akhir
        )

    except ValueError:
        return

    if idx_new > idx_now:

        alat_repository.update_kondisi_fisik(
            db,
            alat_id,
            kondisi_akhir,
        )