# app/schemas/pengembalian.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.constants.enums import (
    StatusVerifikasiPengembalian,
    KondisiFisik,
)

class PengembalianDetailItem(BaseModel):

    detail_peminjaman_id: int
    alat_id: int
    jumlah: int

    kondisi_akhir: KondisiFisik

    catatan_pengembalian: Optional[str] = None

class PengembalianCreate(BaseModel):

    peminjaman_id: int

    denda: Decimal = Field(default=Decimal("0.00"))

    catatan: Optional[str] = None

    detail: list[PengembalianDetailItem]

class PengembalianVerify(BaseModel):

    status_verifikasi: StatusVerifikasiPengembalian

    catatan: Optional[str] = None

class PengembalianResponse(BaseModel):

    id: int

    peminjaman_id: int

    diterima_oleh: Optional[int] = None

    tanggal_dikembalikan: datetime

    denda: Decimal

    status_verifikasi: StatusVerifikasiPengembalian

    catatan: Optional[str] = None

    created_at: datetime

    class Config:
        from_attributes = True