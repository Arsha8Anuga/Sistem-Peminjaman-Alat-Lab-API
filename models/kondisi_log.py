from sqlalchemy import Column, Integer, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database.base import Base
from app.constants.enums import KondisiFisik


class KondisiLog(Base):

    __tablename__ = "kondisi_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    alat_id = Column(Integer, ForeignKey("alat.id"), nullable=False)

    peminjaman_id = Column(Integer, ForeignKey("peminjaman.id"), nullable=False)

    kondisi = Column(Enum(KondisiFisik), nullable=False)

    catatan_kerusakan = Column(Text, nullable=True)

    dicatat_oleh = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


    alat = relationship(
        "Alat", 
        back_populates="kondisi_log"
    )

    peminjaman = relationship(
        "Peminjaman", 
        back_populates="kondisi_log"
    )

    pencatat = relationship(
        "User", 
        back_populates="kondisi_log"
    )