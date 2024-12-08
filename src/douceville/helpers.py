from datetime import datetime, timedelta
from datetime import timezone

import jwt
from fastapi import Header, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError

from .config import config
from .schemas import DvUser


def create_access_token(*, data: DvUser, exp: int = None) -> str:
    to_encode = data.model_dump()
    if exp is not None:
        to_encode.update({"exp": exp})
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=60)
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
        print(payload)
        try:
            token_data = DvUser(**payload)
            return token_data
        except ValidationError:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception
