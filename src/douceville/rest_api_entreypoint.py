# https://dev.to/fuegoio/demystifying-authentication-with-fastapi-and-a-frontend-26f5
from urllib.parse import urlencode, parse_qsl
from typing import Dict

import httpx
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

from .config import config
from .helpers import generate_token, create_access_token
from .schemas import (
    EtablissementPublicAvecResultats,
    get_db,
    Url,
    AuthorizationResponse,
    GithubUser,
    DvUser,
    Token,
)
from .crud import get_user_by_login, create_user, get_user, get_etab
from .dependency import get_user_from_header


# curl http://127.0.0.1:3566/login
# curl http://127.0.0.1:3566/authorize -X POST -d '{"code":"dc3606a56ce52309333e","state":"a"}'  -H "Content-Type: application/json"
# curl http://localhost:3566/me -H "Authorization: Bearer "
# curl http://localhost:3566/etablissement/1 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6InlkZXRoZSIsImNvbXBhbnkiOm51bGwsImxvY2F0aW9uIjoiVG91bG91c2UsIEZyYW5jZSIsImVtYWlsIjpudWxsLCJoYXNoZWRfcHdkIjpudWxsLCJhY3RpdmUiOmZhbHNlLCJpZCI6MSwibmFtZSI6Illhbm4gZGUgVGhcdTAwZTkiLCJhdmF0YXJfdXJsIjoiaHR0cHM6Ly9hdmF0YXJzLmdpdGh1YnVzZXJjb250ZW50LmNvbS91LzQ5ODUxNz92PTQiLCJhZG1pbiI6ZmFsc2UsImV4cCI6MTczMzUwMjg3Mn0.W8Hx8PgZFXyxvz87-2KYVFiVdvmcaSPGXshONizDJ8Y"

LOGIN_URL = "https://github.com/login/oauth/authorize"
REDIRECT_URL = f"{config.PROTOCOL}://{config.HOST}/auth/github"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_URL = "https://api.github.com/user"

app = FastAPI()
router = APIRouter()


@router.get("/login", response_model=Url)
def get_login_url() -> Url:
    params = {
        "client_id": config.GITHUB_CLIENT_ID,
        "redirect_uri": REDIRECT_URL,
        "state": generate_token(),
    }
    return Url(url=f"{LOGIN_URL}?{urlencode(params)}")


@router.get("/auth/github", response_model=AuthorizationResponse)
def github_callback(state: str, code: str) -> AuthorizationResponse:
    return AuthorizationResponse(state=state, code=code)


@router.post("/authorize", response_model=Token)
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
        # {'login': 'ydethe', 'id': 498517, 'node_id': 'MDQ6VXNlcjQ5ODUxNw==', 'avatar_url': 'https://avatars.githubusercontent.com/u/498517?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/ydethe', 'html_url': 'https://github.com/ydethe', 'followers_url': 'https://api.github.com/users/ydethe/followers', 'following_url': 'https://api.github.com/users/ydethe/following{/other_user}', 'gists_url': 'https://api.github.com/users/ydethe/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/ydethe/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/ydethe/subscriptions', 'organizations_url': 'https://api.github.com/users/ydethe/orgs', 'repos_url': 'https://api.github.com/users/ydethe/repos', 'events_url': 'https://api.github.com/users/ydethe/events{/privacy}', 'received_events_url': 'https://api.github.com/users/ydethe/received_events', 'type': 'DvUser', 'user_view_type': 'private', 'site_admin': False, 'name': 'Yann de Thé', 'company': None, 'blog': '', 'location': 'Toulouse, France', 'email': None, 'hireable': None, 'bio': 'I love to perform innovative data analysis to provide quantitive assessment of a problem. I love applying it to the space industry !', 'twitter_username': None, 'notification_email': None, 'public_repos': 28, 'public_gists': 0, 'followers': 2, 'following': 1, 'created_at': '2010-11-27T00:40:38Z', 'updated_at': '2024-09-29T17:28:01Z', 'private_gists': 0, 'total_private_repos': 19, 'owned_private_repos': 19, 'disk_usage': 116128, 'collaborators': 0, 'two_factor_authentication': True, 'plan': {'name': 'free', 'space': 976562499, 'collaborators': 0, 'private_repos': 10000}}
        github_user = GithubUser(**user_request.json())

    db_user = get_user_by_login(db, github_user.login)
    if db_user is None:
        db_user = create_user(db, github_user)

    access_token = create_access_token(data=db_user)

    return Token(access_token=access_token, token_type="bearer", user=db_user)


@router.get("/me", response_model=DvUser)
def read_profile(
    user: DvUser = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> DvUser:
    db_user = get_user(db, user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="DvUser not found")
    return db_user


@router.get("/etablissement/{etab_id}", response_model=EtablissementPublicAvecResultats)
def read_etablissement(
    etab_id: int,
    user: DvUser = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> DvUser:
    db_user = get_user(db, user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="DvUser not found")
    etab = get_etab(db, etab_id)
    return etab


app.include_router(router)
