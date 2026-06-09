from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

from app.constants.enums import StatusPeminjaman
from app.schemas.detail_peminjaman import (
    DetailPeminjamanAjukan,
    DetailPeminjamanResponse,
)


class PeminjamanAjukan(BaseModel):
    tanggal_pinjam: date
    tanggal_rencana_kembali: date
    catatan: Optional[str] = None
    detail: List[DetailPeminjamanAjukan] = Field(min_length=1)


class PeminjamanBase(BaseModel):
    kode_peminjaman: str
    mahasiswa_id: int
    disetujui_oleh: Optional[int] = None
    tanggal_pengajuan: datetime
    tanggal_pinjam: date
    tanggal_rencana_kembali: date
    status: StatusPeminjaman
    catatan: Optional[str] = None


class PeminjamanCreate(PeminjamanBase):
    pass


class PeminjamanResponse(PeminjamanBase):
    id: int
    created_at: datetime
    updated_at: datetime
    detail_peminjaman: list[DetailPeminjamanResponse] = []

    class Config:
        from_attributes = True