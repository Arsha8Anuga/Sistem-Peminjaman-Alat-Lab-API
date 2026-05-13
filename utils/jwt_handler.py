from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

def encode_token(data: dict):

    encoded_token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_token

def decode_token(token: str):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return encode_token(to_encode)

def verify_access_token(token: str):

    try:

        payload = decode_token(token)

        return payload

    except JWTError:

        return None