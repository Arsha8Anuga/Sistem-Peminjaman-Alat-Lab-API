from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class KategoriAlatBase(BaseModel):
    nama_kategori: str
    deskripsi: Optional[str] = None

class KategoriAlatCreate(KategoriAlatBase):
    pass

class KategoriAlatResponse(KategoriAlatBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True