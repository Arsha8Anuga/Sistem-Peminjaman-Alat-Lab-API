from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from app.constants import HttpCode
from .response import error_response

def raise_http_exception(
    status_code: int,
    message: str,
) -> None:

    raise HTTPException(
        status_code=status_code,
        detail=message,
    )


def raise_bad_request(
    message: str = "Permintaan tidak valid",
) -> None:

    raise_http_exception(
        HttpCode.BAD_REQUEST,
        message,
    )


def raise_unauthorized(
    message: str = "Autentikasi diperlukan",
) -> None:

    raise_http_exception(
        HttpCode.UNAUTHORIZED,
        message,
    )


def raise_forbidden(
    message: str = "Anda tidak memiliki akses",
) -> None:

    raise_http_exception(
        HttpCode.FORBIDDEN,
        message,
    )


def raise_not_found(
    message: str = "Data tidak ditemukan",
) -> None:

    raise_http_exception(
        HttpCode.NOT_FOUND,
        message,
    )


def raise_conflict(
    message: str = "Data sudah ada",
) -> None:

    raise_http_exception(
        HttpCode.CONFLICT,
        message,
    )


def register_exception_handlers(
    app: FastAPI
) -> None:

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ):

        return error_response(
            message=exc.detail,
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):

        errors = [
            {
                "field": " -> ".join(
                    str(loc)
                    for loc in err["loc"]
                ),
                "message": err["msg"],
            }
            for err in exc.errors()
        ]

        return error_response(
            message="Validasi data gagal",
            status_code=HttpCode.UNPROCESSABLE_ENTITY,
            errors=errors,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception
    ):

        return error_response(
            message="Terjadi kesalahan pada server",
            status_code=HttpCode.INTERNAL_SERVER_ERROR,
        )