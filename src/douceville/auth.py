from fastapi import HTTPException, status, Request
from supabase import create_client
from supabase.lib.client_options import ClientOptions
from jose import jwt
from jose.exceptions import JOSEError

from .schemas import DvUser
from .config import config


def get_token_user(request: Request) -> DvUser:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer not found")

    token = auth_header[7:]

    try:
        payload = jwt.decode(token, config.SUPABASE_JWT_SECRET, audience="authenticated")
    except JOSEError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")

    user_id = payload["sub"]
    user_email = payload["email"]
    # dt_exp=datetime.fromtimestamp(payload['exp'])
    # print(dt_exp)

    # https://supabase.com/docs/reference/python/admin-api
    supabase = create_client(
        config.SUPABASE_URL,
        config.SUPABASE_ADMIN_KEY,
        options=ClientOptions(
            auto_refresh_token=False,
            persist_session=False,
        ),
    )

    response = supabase.table("users").select("*").eq("id", user_id).execute()
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
