# app/utils/file_storage.py
import os
import uuid
from fastapi import UploadFile
from app.config import UPLOAD_DIR

ALLOWED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}

def save_file(file: UploadFile, folder: str) -> str:
    os.makedirs(os.path.join(UPLOAD_DIR, folder), exist_ok=True)

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"

    path = os.path.join(UPLOAD_DIR, folder, filename)

    with open(path, "wb") as buffer:
        buffer.write(file.file.read())

    return path


def delete_file(path: str):
    if path and os.path.exists(path):
        os.remove(path)

def is_valid_image(file: UploadFile):
    filename = file.filename.lower()

    ext = os.path.splitext(filename)[1]
    if ext not in ALLOWED_IMAGE_EXT:
        return False

    if file.content_type not in ALLOWED_MIME:
        return False

    return True