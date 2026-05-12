from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.database.base import Base


class KategoriAlat(Base):

    __tablename__ = "kategori_alat"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    nama_kategori = Column(String(100), unique=True, nullable=False)

    deskripsi = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))


    alat = relationship(
        "Alat",
        back_populates="kategori",
        lazy="selectin",
    )