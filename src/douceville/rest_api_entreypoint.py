# https://dev.to/fuegoio/demystifying-authentication-with-fastapi-and-a-frontend-26f5
from urllib.parse import urlencode, parse_qsl
from typing import Dict

import httpx
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

from .config import config
from .helpers import generate_token, create_access_token
from .schemas import Url, AuthorizationResponse, GithubUser, User, Token
from .crud import get_user_by_login, create_user, get_user
from .dependency import get_user_from_header
from .models import User as DbUser, get_db
from .app import app as DvApp  # noqa: F401


# curl http://127.0.0.1:3566/login
# curl http://127.0.0.1:3566/authorize -X POST -d '{"code":"65d51c4041a2dcfb7347","state":"a"}'  -H "Content-Type: application/json"
# curl http://localhost:3566/me -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibG9naW4iOiJ5ZGV0aGUiLCJuYW1lIjpudWxsLCJjb21wYW55IjpudWxsLCJsb2NhdGlvbiI6bnVsbCwiZW1haWwiOiJ5ZGV0aGVAZ21haWwuY29tIiwiYXZhdGFyX3VybCI6bnVsbCwiaGFzaGVkX3B3ZCI6IiQyYiQxMCQzcTFIQVNOcENOU1pkenVSMlc5cE1laEJ3UWlTUlZRTDdTa0gxMTJOQk9ueHdpU29oSjJ6MiIsImFkbWluIjp0cnVlLCJhY3RpdmUiOnRydWUsInN0cmlwZV9pZCI6bnVsbCwiZXhwIjoxNzMzNDk3NDIzfQ.j2bYZVdVLXAa0-uSer-dylgTIblT2pPzyZHjhWNJPPc"

LOGIN_URL = "https://github.com/login/oauth/authorize"
REDIRECT_URL = f"{config.PROTOCOL}://{config.HOST}/auth/github"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_URL = "https://api.github.com/user"

app = FastAPI()
router = APIRouter()


@router.get("/login")
def get_login_url() -> Url:
    params = {
        "client_id": config.GITHUB_CLIENT_ID,
        "redirect_uri": REDIRECT_URL,
        "state": generate_token(),
    }
    return Url(url=f"{LOGIN_URL}?{urlencode(params)}")


@router.get("/auth/github")
def github_callback(state: str, code: str) -> AuthorizationResponse:
    return AuthorizationResponse(state=state, code=code)


@router.post("/authorize")
async def verify_authorization(body: AuthorizationResponse, db: Session = Depends(get_db)) -> Token:
    params = {
        "client_id": config.GITHUB_CLIENT_ID,
        "client_secret": config.GITHUB_CLIENT_SECRET,
        "code": body.code,
        "state": body.state,
    }

    async with httpx.AsyncClient() as client:
        token_request = await client.post(TOKEN_URL, params=params)
        response: Dict[bytes, bytes] = dict(parse_qsl(token_request.content))
        github_token = response[b"access_token"].decode("utf-8")
        github_header = {"Authorization": f"token {github_token}"}
        user_request = await client.get(USER_URL, headers=github_header)
        # print(user_request.json())
        # {'login': 'ydethe', 'id': 498517, 'node_id': 'MDQ6VXNlcjQ5ODUxNw==', 'avatar_url': 'https://avatars.githubusercontent.com/u/498517?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/ydethe', 'html_url': 'https://github.com/ydethe', 'followers_url': 'https://api.github.com/users/ydethe/followers', 'following_url': 'https://api.github.com/users/ydethe/following{/other_user}', 'gists_url': 'https://api.github.com/users/ydethe/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/ydethe/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/ydethe/subscriptions', 'organizations_url': 'https://api.github.com/users/ydethe/orgs', 'repos_url': 'https://api.github.com/users/ydethe/repos', 'events_url': 'https://api.github.com/users/ydethe/events{/privacy}', 'received_events_url': 'https://api.github.com/users/ydethe/received_events', 'type': 'User', 'user_view_type': 'private', 'site_admin': False, 'name': 'Yann de Thé', 'company': None, 'blog': '', 'location': 'Toulouse, France', 'email': None, 'hireable': None, 'bio': 'I love to perform innovative data analysis to provide quantitive assessment of a problem. I love applying it to the space industry !', 'twitter_username': None, 'notification_email': None, 'public_repos': 28, 'public_gists': 0, 'followers': 2, 'following': 1, 'created_at': '2010-11-27T00:40:38Z', 'updated_at': '2024-09-29T17:28:01Z', 'private_gists': 0, 'total_private_repos': 19, 'owned_private_repos': 19, 'disk_usage': 116128, 'collaborators': 0, 'two_factor_authentication': True, 'plan': {'name': 'free', 'space': 976562499, 'collaborators': 0, 'private_repos': 10000}}
        github_user = GithubUser(**user_request.json())

    db_user = get_user_by_login(db, github_user.login)
    if db_user is None:
        db_user = create_user(db, github_user)

    verified_user = User.model_validate(db_user, from_attributes=True)
    access_token = create_access_token(data=verified_user)

    return Token(access_token=access_token, token_type="bearer", user=verified_user)


@router.get("/me", response_model=User)
def read_profile(
    user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> DbUser:
    db_user = get_user(db, user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


app.include_router(router)
