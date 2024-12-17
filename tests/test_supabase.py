import asyncio

import pytest
from fastapi import Request
from starlette.datastructures import Headers

from douceville.config import config
from douceville.auth import SupabaseAuth
from douceville.auth import create_access_token


@pytest.mark.asyncio
async def test_supabase():
    # ==========================
    # Frontend behaviour
    # ==========================
    token = create_access_token(
        config.SUPABASE_URL,
        config.SUPABASE_KEY,
        config.SUPABASE_TEST_USER,
        config.SUPABASE_TEST_PASSWORD,
    )
    print(token)

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
