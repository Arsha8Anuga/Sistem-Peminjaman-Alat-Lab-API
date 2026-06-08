# app/schemas/peminjaman.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

from app.constants.enums import StatusPeminjaman, KondisiFisik

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

class DetailAjukan(BaseModel):

    alat_id: int
    jumlah: int
    kondisi_awal: KondisiFisik = KondisiFisik.BAIK


class PeminjamanAjukan(BaseModel):
  
    tanggal_pinjam: date
    tanggal_rencana_kembali: date
    catatan: Optional[str] = None
    detail: List[DetailAjukan]