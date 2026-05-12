class ResponseMessage:

    SUCCESS = "Berhasil"
    CREATED = "Data berhasil ditambahkan"
    UPDATED = "Data berhasil diperbarui"
    DELETED = "Data berhasil dihapus"
    NOT_FOUND = "Data tidak ditemukan"
    BAD_REQUEST = "Permintaan tidak valid"
    UNAUTHORIZED = "Autentikasi diperlukan"
    FORBIDDEN = "Anda tidak memiliki akses"
    SERVER_ERROR = "Terjadi kesalahan pada server"

    LOGIN_SUCCESS = "Login berhasil"
    LOGIN_FAILED = "Email atau password salah"
    TOKEN_INVALID = "Token tidak valid atau sudah kedaluwarsa"
    TOKEN_EXPIRED = "Token sudah kedaluwarsa"
    LOGOUT_SUCCESS = "Logout berhasil"
    REGISTER_SUCCESS = "Registrasi berhasil"

    USER_NOT_FOUND = "User tidak ditemukan"
    EMAIL_TAKEN = "Email sudah digunakan"
    NIM_NIP_TAKEN = "NIM/NIP sudah terdaftar"

    ALAT_NOT_FOUND = "Alat tidak ditemukan"
    ALAT_CREATED = "Alat berhasil ditambahkan"
    ALAT_UPDATED = "Alat berhasil diperbarui"
    ALAT_DELETED = "Alat berhasil dihapus"
    STOK_TIDAK_CUKUP = "Stok alat tidak mencukupi"

    KATEGORI_NOT_FOUND = "Kategori tidak ditemukan"
    KATEGORI_CREATED = "Kategori berhasil ditambahkan"
    KATEGORI_UPDATED = "Kategori berhasil diperbarui"
    KATEGORI_DELETED = "Kategori berhasil dihapus"

    PEMINJAMAN_NOT_FOUND = "Peminjaman tidak ditemukan"
    PEMINJAMAN_CREATED = "Pengajuan peminjaman berhasil dikirim"
    PEMINJAMAN_DISETUJUI = "Peminjaman berhasil disetujui"
    PEMINJAMAN_DITOLAK = "Peminjaman ditolak"
    PEMINJAMAN_DIPINJAM = "Alat berhasil diambil"
    PEMINJAMAN_DIBATALKAN = "Peminjaman berhasil dibatalkan"
    PEMINJAMAN_INVALID_STATUS = (
        "Perubahan status tidak diizinkan"
    )

    PENGEMBALIAN_SUCCESS = "Pengembalian berhasil dicatat"
    PENGEMBALIAN_VERIFIED = (
        "Pengembalian berhasil diverifikasi"
    )
    PENGEMBALIAN_NOT_FOUND = (
        "Data pengembalian tidak ditemukan"
    )