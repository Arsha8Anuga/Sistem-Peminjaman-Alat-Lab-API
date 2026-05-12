from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.constants.enums import KondisiFisik


class KondisiLogBase(BaseModel):
    alat_id: int
    peminjaman_id: int
    kondisi: KondisiFisik
    catatan_kerusakan: Optional[str] = None
    dicatat_oleh: int


class KondisiLogCreate(KondisiLogBase):
    pass


class KondisiLogResponse(KondisiLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True