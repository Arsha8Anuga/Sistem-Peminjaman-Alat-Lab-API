from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, Text, Enum, DECIMAL, Integer
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime, timezone
from app.constants.enums import StatusVerifikasiPengembalian


class Pengembalian(Base):

    __tablename__ = "pengembalian"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    peminjaman_id = Column(Integer, ForeignKey("peminjaman.id"), nullable=False)

    diterima_oleh = Column(Integer, ForeignKey("users.id"), nullable=False)

    tanggal_dikembalikan = Column(DateTime, nullable=False)

    denda = Column(DECIMAL(10, 2), default=0, nullable=False)

    status_verifikasi = Column(
        Enum(StatusVerifikasiPengembalian),
        default=StatusVerifikasiPengembalian.MENUNGGU,
        nullable=False,
    )

    catatan = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    
    peminjaman = relationship(
        "Peminjaman",
        back_populates="pengembalian",
    )

    penerima = relationship(
        "User",
        back_populates="pengembalian_diterima",
    )