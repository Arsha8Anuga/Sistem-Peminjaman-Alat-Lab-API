from sqlalchemy import create_engine
from app.config import DATABASE_URL


def _create_engine():
    url = DATABASE_URL or "sqlite:///./lab_borrowing.db"

    kwargs = {
        "pool_pre_ping": True,
        "echo": False,
    }

    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}

    return create_engine(url, **kwargs)


engine = _create_engine()
