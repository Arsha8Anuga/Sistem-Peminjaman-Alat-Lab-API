from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.constants.enums import KondisiFisik, StatusKetersediaan

class AlatBase(BaseModel):
    kategori_id: int
    kode_alat: str
    nama_alat: str
    merk: Optional[str] = None
    spesifikasi: Optional[str] = None
    lokasi_penyimpanan: str
    stok_total: int
    stok_tersedia: int
    kondisi_fisik: KondisiFisik
    status_ketersediaan: StatusKetersediaan
    foto: Optional[str] = None
    deskripsi: Optional[str] = None

class AlatCreate(AlatBase):
    pass

class AlatUpdate(BaseModel):
    kategori_id: Optional[int] = None
    kode_alat: Optional[str] = None
    nama_alat: Optional[str] = None
    merk: Optional[str] = None
    spesifikasi: Optional[str] = None
    lokasi_penyimpanan: Optional[str] = None
    stok_total: Optional[int] = None
    stok_tersedia: Optional[int] = None
    deskripsi: Optional[str] = None
    foto: Optional[str] = None
    

class AlatResponse(AlatBase):

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True