from fastapi import HTTPException, status, Request
from supabase import create_client, Client
from jose import jwt

from .schemas import DvUser
from .config import config


def get_token_user(request: Request) -> DvUser:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer not found")

    token = auth_header[7:]

    payload = jwt.decode(token, config.SUPABASE_JWT_SECRET, audience="authenticated")
    user_id = payload["sub"]
    user_email = payload["email"]

    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    supabase.auth.sign_in_with_password(
        {"email": config.SUPABASE_TEST_USER, "password": config.SUPABASE_TEST_PASSWORD}
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
