from enum import Enum

class UserRole(str, Enum):

    MAHASISWA = "mahasiswa"
    LABORAN = "laboran"
    ASISTEN = "asisten"
    ADMIN = "admin"

class StatusPeminjaman(str, Enum):

    PENDING = "pending"
    DISETUJUI = "disetujui"
    DITOLAK = "ditolak"
    DIPINJAM = "dipinjam"
    DIKEMBALIKAN = "dikembalikan"
    SELESAI = "selesai"
    DIBATALKAN = "dibatalkan"

class KondisiFisik(str, Enum):

    BAIK = "baik"
    RUSAK_RINGAN = "rusak_ringan"
    RUSAK_BERAT = "rusak_berat"
    MAINTENANCE = "maintenance"
    HILANG = "hilang"

class StatusKetersediaan(str, Enum):

    TERSEDIA = "tersedia"
    DIPINJAM = "dipinjam"
    MAINTENANCE = "maintenance"

class StatusVerifikasiPengembalian(str, Enum):
    
    MENUNGGU = "menunggu"
    SESUAI = "sesuai"
    RUSAK = "rusak"
    HILANG = "hilang"