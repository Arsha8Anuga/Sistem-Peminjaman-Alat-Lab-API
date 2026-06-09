import uuid
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import peminjaman_repository, alat_repository
from app.constants import HttpCode, ResponseMessage
from app.constants.enums import StatusPeminjaman, UserRole


def _generate_kode_peminjaman() -> str:
    tanggal = datetime.now(timezone.utc).strftime("%Y%m%d")
    suffix = uuid.uuid4().hex[:4].upper()
    return f"PJM-{tanggal}-{suffix}"


def _get_peminjaman_or_404(db: Session, peminjaman_id: int):
    data = peminjaman_repository.get_peminjaman_by_id(db, peminjaman_id)
    if not data:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.PEMINJAMAN_NOT_FOUND,
        )
    return data


def _get_alat_or_404(db: Session, alat_id: int):
    alat = alat_repository.get_alat_by_id(db, alat_id)
    if not alat:
        raise HTTPException(
            status_code=HttpCode.NOT_FOUND,
            detail=ResponseMessage.ALAT_NOT_FOUND,
        )
    return alat


def get_all_peminjaman(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    current_user=None,
):
    if current_user and current_user.role == UserRole.MAHASISWA:
        return peminjaman_repository.get_peminjaman_by_mahasiswa_id(
            db,
            current_user.id,
        )

    return peminjaman_repository.get_all_peminjaman(
        db,
        page=page,
        page_size=page_size,
    )


def get_peminjaman_by_id(db: Session, peminjaman_id: int, current_user=None):
    peminjaman = _get_peminjaman_or_404(db, peminjaman_id)

    if current_user and current_user.role == UserRole.MAHASISWA:
        if peminjaman.mahasiswa_id != current_user.id:
            raise HTTPException(
                status_code=HttpCode.FORBIDDEN,
                detail=ResponseMessage.FORBIDDEN,
            )

    return peminjaman


def get_peminjaman_by_mahasiswa(db: Session, mahasiswa_id: int):
    return peminjaman_repository.get_peminjaman_by_mahasiswa_id(db, mahasiswa_id)


def ajukan_peminjaman(db: Session, mahasiswa_id: int, peminjaman_data):
    try:
        if peminjaman_data.tanggal_rencana_kembali < peminjaman_data.tanggal_pinjam:
            raise HTTPException(
                status_code=HttpCode.BAD_REQUEST,
                detail="Tanggal rencana kembali tidak boleh lebih awal dari tanggal pinjam.",
            )

        for detail in peminjaman_data.detail:
            alat = _get_alat_or_404(db, detail.alat_id)
            if alat.stok_tersedia < detail.jumlah:
                raise HTTPException(
                    status_code=HttpCode.BAD_REQUEST,
                    detail=f"{ResponseMessage.STOK_TIDAK_CUKUP}: {alat.nama_alat}",
                )

        new_data = peminjaman_repository.create_peminjaman(
            db,
            mahasiswa_id=mahasiswa_id,
            kode_peminjaman=_generate_kode_peminjaman(),
            tanggal_pinjam=peminjaman_data.tanggal_pinjam,
            tanggal_rencana_kembali=peminjaman_data.tanggal_rencana_kembali,
            catatan=peminjaman_data.catatan,
            detail_list=peminjaman_data.detail,
        )

        db.commit()
        db.refresh(new_data)
        return new_data

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def setujui_peminjaman(db: Session, peminjaman_id: int, laboran_id: int):
    peminjaman = _get_peminjaman_or_404(db, peminjaman_id)

    if peminjaman.status != StatusPeminjaman.PENDING:
        raise HTTPException(
            status_code=HttpCode.BAD_REQUEST,
            detail=ResponseMessage.PEMINJAMAN_INVALID_STATUS,
        )

    try:
        for detail in peminjaman.detail_peminjaman:
            alat = _get_alat_or_404(db, detail.alat_id)
            if alat.stok_tersedia < detail.jumlah:
                raise HTTPException(
                    status_code=HttpCode.BAD_REQUEST,
                    detail=f"{ResponseMessage.STOK_TIDAK_CUKUP}: {alat.nama_alat}",
                )

        for detail in peminjaman.detail_peminjaman:
            alat_repository.kurangi_stok(db, detail.alat_id, detail.jumlah)

        updated = peminjaman_repository.update_status_peminjaman(
            db,
            peminjaman_id=peminjaman_id,
            status=StatusPeminjaman.DISETUJUI,
            disetujui_oleh=laboran_id,
        )

        db.commit()
        db.refresh(updated)
        return updated

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def tolak_peminjaman(db: Session, peminjaman_id: int, catatan: str = ""):
    peminjaman = _get_peminjaman_or_404(db, peminjaman_id)

    if peminjaman.status != StatusPeminjaman.PENDING:
        raise HTTPException(
            status_code=HttpCode.BAD_REQUEST,
            detail=ResponseMessage.PEMINJAMAN_INVALID_STATUS,
        )

    try:
        updated = peminjaman_repository.update_status_peminjaman(
            db,
            peminjaman_id=peminjaman_id,
            status=StatusPeminjaman.DITOLAK,
            catatan=catatan,
        )
        db.commit()
        db.refresh(updated)
        return updated

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def ambil_alat(db: Session, peminjaman_id: int):
    peminjaman = _get_peminjaman_or_404(db, peminjaman_id)

    if peminjaman.status != StatusPeminjaman.DISETUJUI:
        raise HTTPException(
            status_code=HttpCode.BAD_REQUEST,
            detail=ResponseMessage.PEMINJAMAN_INVALID_STATUS,
        )

    try:
        updated = peminjaman_repository.update_status_peminjaman(
            db,
            peminjaman_id=peminjaman_id,
            status=StatusPeminjaman.DIPINJAM,
        )
        db.commit()
        db.refresh(updated)
        return updated

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def batalkan_peminjaman(db: Session, peminjaman_id: int, mahasiswa_id: int):
    peminjaman = _get_peminjaman_or_404(db, peminjaman_id)

    if peminjaman.mahasiswa_id != mahasiswa_id:
        raise HTTPException(
            status_code=HttpCode.FORBIDDEN,
            detail=ResponseMessage.FORBIDDEN,
        )

    if peminjaman.status != StatusPeminjaman.PENDING:
        raise HTTPException(
            status_code=HttpCode.BAD_REQUEST,
            detail=ResponseMessage.PEMINJAMAN_INVALID_STATUS,
        )

    try:
        updated = peminjaman_repository.update_status_peminjaman(
            db,
            peminjaman_id=peminjaman_id,
            status=StatusPeminjaman.DIBATALKAN,
        )
        db.commit()
        db.refresh(updated)
        return updated

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
