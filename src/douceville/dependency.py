import jwt
from fastapi import Header, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError

from .config import config
from .schemas import DvUser


def get_user_from_header(*, authorization: str = Header(None)) -> DvUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    scheme, token = get_authorization_scheme_param(authorization)
    print(scheme, token)
    if scheme.lower() != "bearer":
        raise credentials_exception

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        try:
            token_data = DvUser(**payload)
            return token_data
        except ValidationError:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
