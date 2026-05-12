from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.database.base import Base
from app.constants.enums import KondisiFisik, StatusKetersediaan


class Alat(Base):

    __tablename__ = "alat"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    kategori_id = Column(Integer, ForeignKey("kategori_alat.id"), nullable=False)

    kode_alat = Column(String(50), unique=True, nullable=False)

    nama_alat = Column(String(100), nullable=False)

    merk = Column(String(100), nullable=True)

    spesifikasi = Column(Text, nullable=True)

    lokasi_penyimpanan = Column(String(100), nullable=False)

    stok_total = Column(Integer, nullable=False, default=0)

    stok_tersedia = Column(Integer, nullable=False, default=0)

    kondisi_fisik = Column(Enum(KondisiFisik), nullable=False)

    status_ketersediaan = Column(Enum(StatusKetersediaan), nullable=False)

    foto = Column(String(255), nullable=True)

    deskripsi = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


    kategori = relationship("KategoriAlat", back_populates="alat")

    detail_peminjaman = relationship("DetailPeminjaman", back_populates="alat", lazy="selectin")

    kondisi_log = relationship("KondisiLog", back_populates="alat", lazy="selectin")