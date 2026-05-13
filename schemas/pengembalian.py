from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.constants.enums import (
    StatusVerifikasiPengembalian
)


# =========================================================
# BASE
# =========================================================
class PengembalianBase(BaseModel):

    peminjaman_id: int
    tanggal_dikembalikan: datetime
    denda: Decimal = Field(
        default=Decimal("0.00")
    )

    catatan: Optional[str] = None


# =========================================================
# CREATE
# staff input pengembalian
# =========================================================
class PengembalianCreate(PengembalianBase):
    pass


# =========================================================
# VERIFY
# admin/laboran verify kondisi
# =========================================================
class PengembalianVerify(BaseModel):

    status_verifikasi: StatusVerifikasiPengembalian
    catatan: Optional[str] = None


# =========================================================
# RESPONSE
# =========================================================
class PengembalianResponse(PengembalianBase):

    id: int
    diterima_oleh: int
    status_verifikasi: StatusVerifikasiPengembalian
    created_at: datetime

    class Config:
        from_attributes = True