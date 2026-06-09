from pydantic import BaseModel, Field
from typing import Optional

from app.constants.enums import KondisiFisik

class DetailPeminjamanAjukan(BaseModel):
    alat_id: int
    jumlah: int = Field(gt=0)


class DetailPeminjamanBase(BaseModel):
    peminjaman_id: int
    alat_id: int
    jumlah: int
    kondisi_awal: Optional[KondisiFisik] = None
    kondisi_akhir: Optional[KondisiFisik] = None
    catatan_pengembalian: Optional[str] = None


class DetailPeminjamanCreate(DetailPeminjamanBase):
    pass


class DetailPeminjamanResponse(DetailPeminjamanBase):
    id: int

    class Config:
        from_attributes = True
