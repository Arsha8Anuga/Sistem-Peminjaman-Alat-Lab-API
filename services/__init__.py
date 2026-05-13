from .auth_service import login_user, register_user
from .user_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
)
from .alat_service import (
    get_all_alat,
    get_alat_by_id,
    create_alat,
    update_alat,
    delete_alat,
)
from .kategori_service import (
    get_all_kategori,
    get_kategori_by_id,
    create_kategori,
    update_kategori,
    delete_kategori,
)
from .peminjaman_service import (
    ajukan_peminjaman,
    setujui_peminjaman,
    tolak_peminjaman,
    ambil_alat,
    batalkan_peminjaman,
    get_all_peminjaman,
    get_peminjaman_by_id,
    get_peminjaman_by_mahasiswa,
)
from .pengembalian_service import (
    catat_pengembalian,
    verifikasi_pengembalian,
    get_pengembalian_by_peminjaman,
)

__all__ = [
    # auth
    "login_user",
    "register_user",
    # user
    "get_all_users",
    "get_user_by_id",
    "update_user",
    "delete_user",
    # alat
    "get_all_alat",
    "get_alat_by_id",
    "create_alat",
    "update_alat",
    "delete_alat",
    # kategori
    "get_all_kategori",
    "get_kategori_by_id",
    "create_kategori",
    "update_kategori",
    "delete_kategori",
    # peminjaman
    "ajukan_peminjaman",
    "setujui_peminjaman",
    "tolak_peminjaman",
    "ambil_alat",
    "batalkan_peminjaman",
    "get_all_peminjaman",
    "get_peminjaman_by_id",
    "get_peminjaman_by_mahasiswa",
    # pengembalian
    "catat_pengembalian",
    "verifikasi_pengembalian",
    "get_pengembalian_by_peminjaman",
]