from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from app.constants.enums import (
    KondisiFisik,
    StatusVerifikasiPengembalian,
)


class PengembalianDetailCreate(BaseModel):
    detail_peminjaman_id: int
    alat_id: int
    jumlah: int = Field(gt=0)
    kondisi_akhir: KondisiFisik
    catatan_pengembalian: Optional[str] = None


class PengembalianBase(BaseModel):
    peminjaman_id: int
    tanggal_dikembalikan: Optional[datetime] = None
    denda: Decimal = Field(default=Decimal("0.00"))
    catatan: Optional[str] = None


class PengembalianCreate(PengembalianBase):
    detail: List[PengembalianDetailCreate] = Field(default_factory=list)


class PengembalianVerify(BaseModel):
    status_verifikasi: StatusVerifikasiPengembalian
    catatan: Optional[str] = None


class PengembalianResponse(BaseModel):
    id: int
    peminjaman_id: int
    diterima_oleh: int
    tanggal_dikembalikan: datetime
    denda: Decimal
    status_verifikasi: StatusVerifikasiPengembalian
    catatan: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
