from sqlalchemy import Column, BigInteger, String, Date, DateTime, ForeignKey, Enum, Text, Integer
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database.base import Base
from app.constants.enums import StatusPeminjaman


class Peminjaman(Base):

    __tablename__ = "peminjaman"

    id = Column(Integer, primary_key=True, autoincrement=True)

    kode_peminjaman = Column(String(50), unique=True, nullable=False)

    mahasiswa_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    disetujui_oleh = Column(Integer, ForeignKey("users.id"), nullable=True)

    tanggal_pengajuan = Column(DateTime, nullable=False)

    tanggal_pinjam = Column(Date, nullable=False)

    tanggal_rencana_kembali = Column(Date, nullable=False)

    status = Column(
        Enum(StatusPeminjaman),
        default=StatusPeminjaman.PENDING,
        nullable=False,
    )

    catatan = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


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

    pengembalian = relationship(
        "Pengembalian",
        back_populates="peminjaman",
        uselist=False,
    )

    kondisi_log = relationship(
        "KondisiLog",
        back_populates="peminjaman",
        lazy="selectin",
    )