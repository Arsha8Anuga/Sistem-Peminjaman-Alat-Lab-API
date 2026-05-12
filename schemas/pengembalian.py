from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.constants.enums import StatusVerifikasiPengembalian

class PengembalianBase(BaseModel):
    peminjaman_id: int
    diterima_oleh: int
    tanggal_dikembalikan: datetime
    denda: Decimal = Field(default=Decimal("0.00"))
    status_verifikasi: StatusVerifikasiPengembalian
    catatan: Optional[str] = None

class PengembalianCreate(PengembalianBase):
    pass


class PengembalianResponse(PengembalianBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True