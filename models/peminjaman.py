from sqlalchemy import Column, BigInteger, String, Date, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.database.base import Base
from app.constants.enums import StatusPeminjaman


class Peminjaman(Base):

    __tablename__ = "peminjaman"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    kode_peminjaman = Column(String(50), unique=True, nullable=False)

    mahasiswa_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    disetujui_oleh = Column(BigInteger, ForeignKey("users.id"), nullable=True)

    tanggal_pengajuan = Column(DateTime, nullable=False)

    tanggal_pinjam = Column(Date, nullable=False)

    tanggal_rencana_kembali = Column(Date, nullable=False)

    status = Column(
        Enum(StatusPeminjaman),
        default=StatusPeminjaman.PENDING,
        nullable=False,
    )

    catatan = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


    mahasiswa = relationship(
        "User",
        foreign_keys=[mahasiswa_id],
        back_populates="peminjaman_mahasiswa",
    )

    laboran = relationship(
        "User",
        foreign_keys=[disetujui_oleh],
        back_populates="peminjaman_laboran",
    )

    detail_peminjaman = relationship(
        "DetailPeminjaman",
        back_populates="peminjaman",
        lazy="selectin",
    )

    kondisi_log = relationship(
        "KondisiLog",
        back_populates="peminjaman",
        lazy="selectin",
    )