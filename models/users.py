from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database.base import Base
from app.constants.enums import UserRole


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    nama = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(Enum(UserRole), nullable=False)

    nim_nip = Column(String(50), nullable=True)

    no_hp = Column(String(20), nullable=True)

    foto = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


    peminjaman_mahasiswa = relationship(
        "Peminjaman",
        foreign_keys="Peminjaman.mahasiswa_id",
        back_populates="mahasiswa",
        lazy="selectin",
    )

    peminjaman_laboran = relationship(
        "Peminjaman",
        foreign_keys="Peminjaman.disetujui_oleh",
        back_populates="laboran",
        lazy="selectin",
    )

    pengembalian_diterima = relationship(
        "Pengembalian",
        back_populates="penerima",
        lazy="selectin",
    )

    kondisi_log = relationship(
        "KondisiLog",
        back_populates="pencatat",
        lazy="selectin",
    )