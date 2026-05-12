from sqlalchemy import Column, Integer, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.constants.enums import KondisiFisik


class DetailPeminjaman(Base):

    __tablename__ = "detail_peminjaman"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    peminjaman_id = Column(Integer, ForeignKey("peminjaman.id"), nullable=False)

    alat_id = Column(Integer, ForeignKey("alat.id"), nullable=False)

    jumlah = Column(Integer, nullable=False)

    kondisi_awal = Column(Enum(KondisiFisik), nullable=True)

    kondisi_akhir = Column(Enum(KondisiFisik), nullable=True)

    catatan_pengembalian = Column(Text, nullable=True)


    peminjaman = relationship(
        "Peminjaman",
        back_populates="detail_peminjaman",
    )

    alat = relationship(
        "Alat",
        back_populates="detail_peminjaman",
    )