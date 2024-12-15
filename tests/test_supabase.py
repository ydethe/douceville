from supabase import create_client, Client

from douceville.config import config
from douceville.schemas import DvUser


def test_supabase():
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    response = supabase.auth.sign_in_with_password(
        {"email": config.SUPABASE_TEST_USER, "password": config.SUPABASE_TEST_PASSWORD}
    )

    token = response.session.access_token

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

    supabase.auth.sign_out()


if __name__ == "__main__":
    test_supabase()
