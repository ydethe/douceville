from datetime import datetime, timedelta
from datetime import timezone

import jwt
from fastapi import Header, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError

from .config import config
from .schemas import DvUser


def create_access_token(*, data: DvUser) -> str:
    to_encode = data.model_dump()
    dt_now = datetime.now(tz=timezone.utc)
    expire = dt_now + timedelta(day=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def generate_token() -> str:
    return "a"


def get_user_from_header(*, authorization: str = Header(None)) -> DvUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    scheme, token = get_authorization_scheme_param(authorization)

    if scheme.lower() != "bearer":
        raise credentials_exception

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        try:
            exp = payload.pop("exp", None)
            token_data = DvUser(**payload)
            dt_now = datetime.now(tz=timezone.utc)
            if dt_now > exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if not token_data.active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not active",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return token_data
        except ValidationError:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception
