from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import (
    pengembalian_repository,
    peminjaman_repository,
    alat_repository,
)
from app.constants import HttpCode, ResponseMessage
from app.constants.enums import (
    StatusPeminjaman,
    StatusVerifikasiPengembalian,
    KondisiFisik,
)


# ============================================================================
# HELPER
# ============================================================================

def _get_peminjaman_or_404(db: Session, peminjaman_id: int):
    data = peminjaman_repository.get_peminjaman_by_id(db, peminjaman_id)
    if not data:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.PEMINJAMAN_NOT_FOUND,
        )
    return data


# ============================================================================
# READ
# ============================================================================

def get_pengembalian_by_peminjaman(db: Session, peminjaman_id: int):

    data = pengembalian_repository.get_pengembalian_by_peminjaman_id(
        db, peminjaman_id
    )

    if not data:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.PENGEMBALIAN_NOT_FOUND,
        )

    return data


# ============================================================================
# CREATE PENGEMBALIAN
# ============================================================================

def catat_pengembalian(
    db: Session,
    peminjaman_id: int,
    diterima_oleh: int,
    pengembalian_data,
):

    peminjaman = _get_peminjaman_or_404(db, peminjaman_id)

    if peminjaman.status != StatusPeminjaman.DIPINJAM:
        raise HTTPException(
            status_code=HttpCode.BAD_REQUEST,
            detail=ResponseMessage.PEMINJAMAN_INVALID_STATUS,
        )

    try:
        # ------------------------------------------------------------
        # 1. CREATE PENGEMBALIAN
        # ------------------------------------------------------------
        pengembalian = pengembalian_repository.create_pengembalian(
            db,
            peminjaman_id=peminjaman_id,
            diterima_oleh=diterima_oleh,
            tanggal_dikembalikan=datetime.now(timezone.utc),
            denda=pengembalian_data.denda,
            catatan=pengembalian_data.catatan,
            status_verifikasi=StatusVerifikasiPengembalian.MENUNGGU,
        )

        # ------------------------------------------------------------
        # 2. PROCESS DETAIL
        # ------------------------------------------------------------
        for detail in pengembalian_data.detail:

            # update detail peminjaman
            pengembalian_repository.update_kondisi_akhir_detail(
                db,
                detail_id=detail.detail_peminjaman_id,
                kondisi_akhir=detail.kondisi_akhir,
                catatan_pengembalian=detail.catatan_pengembalian,
            )

            # return stock
            alat_repository.tambah_stok(
                db,
                alat_id=detail.alat_id,
                jumlah=detail.jumlah,
            )

            # log kondisi
            alat_repository.catat_kondisi_log(
                db,
                alat_id=detail.alat_id,
                peminjaman_id=peminjaman_id,
                kondisi=detail.kondisi_akhir,
                catatan=detail.catatan_pengembalian,
                dicatat_oleh=diterima_oleh,
            )

            # update kondisi alat (if worse)
            _update_kondisi_fisik_alat_jika_perlu(
                db,
                alat_id=detail.alat_id,
                kondisi_akhir=detail.kondisi_akhir,
            )

        # ------------------------------------------------------------
        # 3. UPDATE PEMINJAMAN STATUS
        # ------------------------------------------------------------
        peminjaman_repository.update_status_peminjaman(
            db,
            peminjaman_id=peminjaman_id,
            status=StatusPeminjaman.DIKEMBALIKAN,
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


# ============================================================================
# VERIFIKASI PENGEMBALIAN
# ============================================================================

def verifikasi_pengembalian(
    db: Session,
    pengembalian_id: int,
    status_verifikasi: StatusVerifikasiPengembalian,
    catatan: str = "",
):

    pengembalian = pengembalian_repository.get_pengembalian_by_id(
        db, pengembalian_id
    )

    if not pengembalian:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.PENGEMBALIAN_NOT_FOUND,
        )

    if pengembalian.status_verifikasi != StatusVerifikasiPengembalian.MENUNGGU:
        raise HTTPException(
            status_code=HttpCode.BAD_REQUEST,
            detail="Status pengembalian tidak valid",
        )

    try:
        # ------------------------------------------------------------
        # UPDATE STATUS VERIFIKASI
        # ------------------------------------------------------------
        updated = pengembalian_repository.update_status_verifikasi(
            db,
            pengembalian_id=pengembalian_id,
            status_verifikasi=status_verifikasi,
            catatan=catatan,
        )

        peminjaman = _get_peminjaman_or_404(db, pengembalian.peminjaman_id)

        # ------------------------------------------------------------
        # SESUAI → SELESAI
        # ------------------------------------------------------------
        if status_verifikasi == StatusVerifikasiPengembalian.SESUAI:
            peminjaman_repository.update_status_peminjaman(
                db,
                peminjaman_id=pengembalian.peminjaman_id,
                status=StatusPeminjaman.SELESAI,
            )

        # ------------------------------------------------------------
        # RUSAK
        # ------------------------------------------------------------
        elif status_verifikasi == StatusVerifikasiPengembalian.RUSAK:
            for detail in peminjaman.detail_peminjaman:
                alat_repository.update_kondisi_fisik(
                    db,
                    alat_id=detail.alat_id,
                    kondisi=KondisiFisik.RUSAK_RINGAN,
                )

        # ------------------------------------------------------------
        # HILANG (FIXED LOGIC)
        # ------------------------------------------------------------
        elif status_verifikasi == StatusVerifikasiPengembalian.HILANG:
            for detail in peminjaman.detail_peminjaman:

                alat_repository.kurangi_stok_total(
                    db,
                    alat_id=detail.alat_id,
                    jumlah=detail.jumlah,
                )

                alat_repository.update_kondisi_fisik(
                    db,
                    alat_id=detail.alat_id,
                    kondisi=KondisiFisik.HILANG,
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


# ============================================================================
# INTERNAL LOGIC
# ============================================================================

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

    alat = alat_repository.get_alat_by_id(db, alat_id)
    if not alat:
        return

    try:
        idx_now = _URUTAN_KONDISI.index(alat.kondisi_fisik)
        idx_new = _URUTAN_KONDISI.index(kondisi_akhir)
    except ValueError:
        return

    if idx_new > idx_now:
        alat_repository.update_kondisi_fisik(
            db,
            alat_id=alat_id,
            kondisi=kondisi_akhir,
        )