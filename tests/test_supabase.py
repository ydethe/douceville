from supabase import create_client, Client
from fastapi import Request
from starlette.datastructures import Headers

from douceville.config import config
from douceville.auth import get_token_user


def test_supabase():
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
    user = get_token_user(request)

    print(user)


if __name__ == "__main__":
    test_supabase()
