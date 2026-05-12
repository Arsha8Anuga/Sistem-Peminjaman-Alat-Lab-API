from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from app.constants.enums import StatusPeminjaman


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

    class Config:
        from_attributes = True