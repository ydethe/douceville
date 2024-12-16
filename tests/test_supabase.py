import asyncio

import pytest
from supabase import create_client, Client
from fastapi import Request
from starlette.datastructures import Headers

from douceville.config import config
from douceville.auth import SupabaseAuth


@pytest.mark.asyncio
async def test_supabase():
    # ==========================
    # Frontend behaviour
    # ==========================
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    response = supabase.auth.sign_in_with_password(
        {"email": config.SUPABASE_TEST_USER, "password": config.SUPABASE_TEST_PASSWORD}
    )

    token = response.session.access_token
    print(token)

    supabase.auth.sign_out()

    # ==========================
    # Backend behaviour
    # ==========================
    request = Request(scope={"type": "http"})
    request._headers = Headers(headers={"Authorization": f"Bearer {token}"})
    auth = SupabaseAuth(
        scheme_name="scheme_name",
        supabase_jwt_secret=config.SUPABASE_JWT_SECRET,
        supabase_url=config.SUPABASE_URL,
        supabase_admin_key=config.SUPABASE_ADMIN_KEY,
    )
    user = await auth(request)

    print(user)


if __name__ == "__main__":
    asyncio.run(test_supabase())
