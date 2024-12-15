from fastapi import Header, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError
from supabase import create_client, Client
from jose import jwt

from .config import config
from .schemas import DvUser


def create_access_token() -> str:
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    response = supabase.auth.sign_in_with_password(
        {"email": config.SUPABASE_TEST_USER, "password": config.SUPABASE_TEST_PASSWORD}
    )

    token = response.session.access_token
    supabase.auth.sign_out()
    return token


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
