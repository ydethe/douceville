from datetime import datetime, timedelta
from datetime import timezone

import jwt

from .config import config
from .schemas import User


def create_access_token(*, data: User, exp: int = None) -> bytes:
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
