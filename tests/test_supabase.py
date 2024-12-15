from supabase import create_client, Client

from douceville.config import config
from douceville.schemas import DvUser


def test_supabase() -> str:
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    response = supabase.auth.sign_in_with_password(
        {"email": config.SUPABASE_TEST_USER, "password": config.SUPABASE_TEST_PASSWORD}
    )

    token = response.session.access_token

    return token


def test_supabase2(
    token: str = "eyJhbGciOiJIUzI1NiIsImtpZCI6IlViLzRXTVplK29NMmNxdEUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3BtdWRobHFkYXphbXVncm1wa2l1LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiIzNGY2OGUwZC1mNTlmLTQyYjgtOGEyZS0wNjY3MjlkYjEzZTgiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM0MjE1Mjc2LCJpYXQiOjE3MzQyMTE2NzYsImVtYWlsIjoieWFubkBqb2huY2xvdWQuZnIiLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7fSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTczNDIxMTY3Nn1dLCJzZXNzaW9uX2lkIjoiODdjZGVjOGEtMTNiOS00MGU4LWJlMDgtODJlZmE4OTUwNWM0IiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.vGv2vCuKKR1xRGn3tpff1uxokj-__sdbAv2AYUKoI3c",
):
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    response = supabase.auth.sign_in_with_password(
        {"email": config.SUPABASE_TEST_USER, "password": config.SUPABASE_TEST_PASSWORD}
    )

    response = supabase.auth.get_user(token)
    user = response.user

    response = supabase.table("users").select("*").eq("id", user.id).execute()

    user_data = response.data[0]

    user = DvUser(
        id=user_data["id"],
        last_name=user_data["last_name"],
        first_name=user_data["first_name"],
        login=user.email,
        permissions=user_data["permissions"],
    )
    print(user)


if __name__ == "__main__":
    token = test_supabase()
    test_supabase2(token)
