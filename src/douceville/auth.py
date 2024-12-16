from typing_extensions import Annotated, Doc
import typing as T

from starlette.status import HTTP_403_FORBIDDEN
from fastapi import HTTPException, status, Request
from fastapi.security.http import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from jose import jwt
from jose.exceptions import JOSEError

from .schemas import DvUser
from .config import config


class SupabaseAuth(HTTPBearer):
    def __init__(
        self,
        *,
        supabase_jwt_secret: Annotated[
            str,
            Doc(
                """
                Supabase JWT secret
                """
            ),
        ],
        supabase_url: Annotated[
            str,
            Doc(
                """
                Supabase instance URL
                """
            ),
        ],
        supabase_admin_key: Annotated[
            str,
            Doc(
                """
                Supabase admin key
                """
            ),
        ],
        bearerFormat: Annotated[T.Optional[str], Doc("Bearer token format.")] = None,
        scheme_name: Annotated[
            T.Optional[str],
            Doc(
                """
                Security scheme name.

                It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        description: Annotated[
            T.Optional[str],
            Doc(
                """
                Security scheme description.

                It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        auto_error: Annotated[
            bool,
            Doc(
                """
                By default, if the HTTP Bearer token is not provided (in an
                `Authorization` header), `HTTPBearer` will automatically cancel the
                request and send the client an error.

                If `auto_error` is set to `False`, when the HTTP Bearer token
                is not available, instead of erroring out, the dependency result will
                be `None`.

                This is useful when you want to have optional authentication.

                It is also useful when you want to have authentication that can be
                provided in one of multiple optional ways (for example, in an HTTP
                Bearer token or in a cookie).
                """
            ),
        ] = True,
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.supabase_jwt_secret = supabase_jwt_secret
        self.supabase_url = supabase_url
        self.supabase_admin_key = supabase_admin_key

    async def __call__(self, request: Request) -> T.Optional[DvUser]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        if not (authorization and scheme and credentials):
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")

        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )

        user = await self.get_token_user(credentials)

        return user

    async def get_token_user(self, token: str) -> DvUser:
        try:
            payload = jwt.decode(token, self.supabase_jwt_secret, audience="authenticated")
        except JOSEError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")

        user_id = payload["sub"]
        user_email = payload["email"]

        # https://supabase.com/docs/reference/python/admin-api
        supabase = create_client(
            self.supabase_url,
            self.supabase_admin_key,
            options=ClientOptions(
                auto_refresh_token=False,
                persist_session=False,
            ),
        )

        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="No user found in Supabase base"
            )

        user_data = response.data[0]

        supabase.auth.sign_out()

        user = DvUser(
            id=user_id,
            last_name=user_data["last_name"],
            first_name=user_data["first_name"],
            login=user_email,
            permissions=user_data["permissions"],
        )

        return user


def create_access_token() -> str:
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    response = supabase.auth.sign_in_with_password(
        {"email": config.SUPABASE_TEST_USER, "password": config.SUPABASE_TEST_PASSWORD}
    )

    token = response.session.access_token
    supabase.auth.sign_out()
    return token


supabase_auth = SupabaseAuth(
    supabase_jwt_secret=config.SUPABASE_JWT_SECRET,
    supabase_url=config.SUPABASE_URL,
    supabase_admin_key=config.SUPABASE_ADMIN_KEY,
)
