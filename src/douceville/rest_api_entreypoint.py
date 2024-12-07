# https://dev.to/fuegoio/demystifying-authentication-with-fastapi-and-a-frontend-26f5
from urllib.parse import urlencode, parse_qsl
import typing as T

import httpx
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlmodel import select

from .geographique import calcIsochrone
from .config import config
from .helpers import generate_token, create_access_token
from .schemas import (
    Etablissement,
    EtablissementPublicAvecResultats,
    Isochrone,
    QueryParameters,
    get_db,
    Url,
    AuthorizationResponse,
    GithubUser,
    DvUser,
    Token,
)
from .crud import get_user_by_login, create_user, get_etab
from .dependency import get_user_from_header


# hypercorn douceville.rest_api_entreypoint:app --bind 0.0.0.0:3566
# curl http://127.0.0.1:3566/login
# curl http://127.0.0.1:3566/authorize -X POST -d '{"code":"<your_code_here>","state":"a"}'  -H "Content-Type: application/json"
# curl http://localhost:3566/me -H "Authorization: Bearer <your_token_here>"
# curl http://localhost:3566/etablissement/0180766K -H "Authorization: Bearer <your_token_here>"

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
        response: T.Dict[bytes, bytes] = dict(parse_qsl(token_request.content))
        github_token = response[b"access_token"].decode("utf-8")
        github_header = {"Authorization": f"token {github_token}"}
        user_request = await client.get(USER_URL, headers=github_header)
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
    return user


@router.get("/etablissement/{uai}", response_model=EtablissementPublicAvecResultats)
def read_etablissement(
    uai: str,
    user: DvUser = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> DvUser:
    etab = get_etab(db, uai)
    # TODO: Handle the case where no etablissement is found. Return NOT FOUND error
    return etab


@router.post("/etablissements", response_model=T.List[EtablissementPublicAvecResultats])
def etablissement_in_zone(
    body: QueryParameters,
    user: DvUser = Depends(get_user_from_header),
    db: Session = Depends(get_db),
):
    stmt = select(Etablissement).where(func.ST_Within(Etablissement.position, body.iso.getGeom()))

    if body.nature is not None and body.nature != []:
        stmt = stmt.where(Etablissement.nature.in_(body.nature))

    if body.secteur is not None and body.secteur != []:
        stmt = stmt.where(Etablissement.secteur.in_(body.secteur))

    a = db.scalars(stmt)

    return list(a)


@router.get("/isochrone", response_model=Isochrone)
def isochrone(
    lat: float,
    lon: float,
    dist: float,
    transp: str = "driving-car",
    user: DvUser = Depends(get_user_from_header),
):
    center = [lon, lat]
    iso = calcIsochrone(center, dist, transp)

    return iso


app.include_router(router)
