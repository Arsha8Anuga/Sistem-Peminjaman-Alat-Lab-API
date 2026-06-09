from fastapi import FastAPI
import uvicorn

from app.database.base import Base
from app.database.session import engine

# Import model agar SQLAlchemy metadata terdaftar sebelum create_all.
from app.models.users import User  # noqa: F401
from app.models.alat import Alat  # noqa: F401
from app.models.kategori_alat import KategoriAlat  # noqa: F401
from app.models.peminjaman import Peminjaman  # noqa: F401
from app.models.detail_peminjaman import DetailPeminjaman  # noqa: F401
from app.models.pengembalian import Pengembalian  # noqa: F401
from app.models.kondisi_log import KondisiLog  # noqa: F401

from app.routes.auth_routes import router as auth_router
from app.routes.alat_routes import router as alat_router
from app.routes.kategori_routes import router as kategori_router
from app.routes.peminjaman_routes import router as peminjaman_router
from app.routes.pengembalian_routes import router as pengembalian_router
from app.routes.upload_routes import router as upload_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Laboratorium Management System",
    description="Sistem peminjaman alat laboratorium",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Lab Borrowing API is running"}


Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(alat_router)
app.include_router(kategori_router)
app.include_router(peminjaman_router)
app.include_router(pengembalian_router)
app.include_router(upload_router)

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
