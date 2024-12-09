from datetime import datetime, timedelta
from datetime import timezone
from random import randint

import jwt
from fastapi import Header, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError

from .config import config
from .schemas import DvUser


def generate_random_string(size: int) -> str:
    bytes_array = [randint(48, 91) for _ in range(size)]
    return "".join([chr(x) for x in bytes_array])


def create_access_token(*, data: DvUser, expire: datetime = None) -> str:
    to_encode = data.model_dump()
    dt_now = datetime.now(tz=timezone.utc)
    if expire is None:
        expire = dt_now + timedelta(days=1)
    to_encode.update({"exp": expire, "salt": generate_random_string(30)})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def generate_token() -> str:
    return "a"


def get_user_from_header(*, authorization: str = Header(None)) -> DvUser:
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )

    scheme, token = get_authorization_scheme_param(authorization)

    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication scheme: '{scheme}'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        try:
            token_data = DvUser(**payload)
            if not token_data.active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not active",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return token_data
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Validation error: '{e}'",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"JWT error: '{e}'",
            headers={"WWW-Authenticate": "Bearer"},
        )
