from typing import Any, Optional
from fastapi.responses import JSONResponse
from app.constants import HttpCode

def success_response(
    data: Any = None,
    message: str = "Berhasil",
    status_code: int = HttpCode.OK,
    meta: Optional[dict] = None,
) -> JSONResponse:

    body: dict = {
        "success": True,
        "message": message,
        "data": data,
    }

    if meta is not None:
        body["meta"] = meta

    return JSONResponse(
        status_code=status_code,
        content=body
    )


def created_response(
    data: Any = None,
    message: str = "Data berhasil ditambahkan",
) -> JSONResponse:

    return success_response(
        data=data,
        message=message,
        status_code=HttpCode.CREATED,
    )


def updated_response(
    data: Any = None,
    message: str = "Data berhasil diperbarui",
) -> JSONResponse:

    return success_response(
        data=data,
        message=message,
        status_code=HttpCode.OK,
    )


def deleted_response(
    message: str = "Data berhasil dihapus",
) -> JSONResponse:

    return success_response(
        data=None,
        message=message,
        status_code=HttpCode.OK,
    )


def error_response(
    message: str = "Terjadi kesalahan",
    status_code: int = HttpCode.BAD_REQUEST,
    errors: Any = None,
) -> JSONResponse:

    body: dict = {
        "success": False,
        "message": message,
        "data": None,
    }

    if errors is not None:
        body["errors"] = errors

    return JSONResponse(
        status_code=status_code,
        content=body
    )


def bad_request_response(
    message: str = "Permintaan tidak valid",
) -> JSONResponse:

    return error_response(
        message=message,
        status_code=HttpCode.BAD_REQUEST,
    )


def unauthorized_response(
    message: str = "Autentikasi diperlukan",
) -> JSONResponse:

    return error_response(
        message=message,
        status_code=HttpCode.UNAUTHORIZED,
    )


def forbidden_response(
    message: str = "Anda tidak memiliki akses",
) -> JSONResponse:

    return error_response(
        message=message,
        status_code=HttpCode.FORBIDDEN,
    )


def not_found_response(
    message: str = "Data tidak ditemukan",
) -> JSONResponse:

    return error_response(
        message=message,
        status_code=HttpCode.NOT_FOUND,
    )


def conflict_response(
    message: str = "Data sudah ada",
) -> JSONResponse:

    return error_response(
        message=message,
        status_code=HttpCode.CONFLICT,
    )


def server_error_response(
    message: str = "Terjadi kesalahan pada server",
) -> JSONResponse:

    return error_response(
        message=message,
        status_code=HttpCode.INTERNAL_SERVER_ERROR,
    )


def paginated_response(
    data: list,
    total: int,
    page: int,
    page_size: int,
    message: str = "Berhasil",
) -> JSONResponse:

    total_pages = (total + page_size - 1) // page_size

    meta = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }

    return success_response(
        data=data,
        message=message,
        meta=meta,
    )