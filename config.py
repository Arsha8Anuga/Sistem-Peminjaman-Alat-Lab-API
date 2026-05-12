# app/config.py

import os

from dotenv import load_dotenv

load_dotenv()


APP_NAME = os.getenv("APP_NAME")

APP_ENV = os.getenv("APP_ENV")

DEBUG = os.getenv("DEBUG", "False") == "True"

APP_HOST = os.getenv("APP_HOST")

APP_PORT = int(
    os.getenv("APP_PORT", 8000)
)


DB_DRIVER = os.getenv("DB_DRIVER")

DB_HOST = os.getenv("DB_HOST")

DB_PORT = int(
    os.getenv("DB_PORT", 3306)
)

DB_NAME = os.getenv("DB_NAME")

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = os.getenv("DATABASE_URL")


SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        30
    )
)


ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "*"
)

UPLOAD_DIR = os.getenv(
    "UPLOAD_DIR",
    "uploads/"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)