import typing as T

import logfire
from fastapi import HTTPException, APIRouter, status, Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from kinde_sdk.kinde_api_client import KindeApiClient
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlmodel import select
from starlette.middleware.sessions import SessionMiddleware

from .geographique import calcIsochrone
from .config import config
from .schemas import (
    Etablissement,
    EtablissementPublicAvecResultats,
    DvUser,
    Isochrone,
    QueryParameters,
    get_db,
)
from .crud import get_etab
from .auth import get_kinde_client, kinde_api_client_params, user_clients


# hypercorn douceville.rest_api_entreypoint:app --bind 0.0.0.0:3566 --reload
# curl http://127.0.0.1:3566/login
# curl http://127.0.0.1:3566/authorize -X POST -d '{"code":"<your_code_here>","state":"a"}'  -H "Content-Type: application/json"
# curl http://localhost:3566/me -H "Authorization: Bearer <your_token_here>"
# curl http://localhost:3566/etablissement/0180766K -H "Authorization: Bearer <your_token_here>"
# https://kinde.com/blog/engineering/how-to-protect-your-fastapi-routes-with-kinde-authentication/

app = FastAPI(
    title="Douceville API",
    summary="Taux de réussite des écoles",
    description="RestFul API pour lister les écoles et leurs taux de réussite aux examens nationaux",
    version="1.0.0",
    root_path=config.API_PATH,
)
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)
router = APIRouter()

logfire.instrument_fastapi(app)


@router.get("/etablissement/{uai}", response_model=EtablissementPublicAvecResultats)
async def read_etablissement(
    uai: str,
    kinde_client: KindeApiClient = Depends(get_kinde_client),
    db: Session = Depends(get_db),
) -> EtablissementPublicAvecResultats:
    etab = get_etab(db, uai)
    # TODO: Handle the case where no etablissement is found. Return NOT FOUND error
    return etab


@router.post("/etablissements", response_model=T.List[EtablissementPublicAvecResultats])
async def etablissement_in_zone(
    body: QueryParameters,
    kinde_client: KindeApiClient = Depends(get_kinde_client),
    db: Session = Depends(get_db),
) -> T.List[EtablissementPublicAvecResultats]:
    stmt = select(Etablissement).where(func.ST_Within(Etablissement.position, body.iso.getGeom()))

    if body.nature is not None and body.nature != []:
        stmt = stmt.where(Etablissement.nature.in_(body.nature))

    if body.secteur is not None and body.secteur != []:
        stmt = stmt.where(Etablissement.secteur.in_(body.secteur))

    a = db.scalars(stmt)

    return list(a)


@router.get("/isochrone", response_model=Isochrone)
async def isochrone(
    lat: float,
    lon: float,
    dist: float,
    transp: str = "driving-car",
    kinde_client: KindeApiClient = Depends(get_kinde_client),
) -> Isochrone:
    center = [lon, lat]
    iso = calcIsochrone(center, dist, transp)

    return iso


@router.get("/user", response_model=DvUser)
async def get_user(
    kinde_client: KindeApiClient = Depends(get_kinde_client),
) -> DvUser:
    user = DvUser(
        id=kinde_client.client_id,
        login=kinde_client.client_id,
        admin=True,
        active=True,
    )

    return user


# Login endpoint
@app.get("/api/auth/login")
def login(request: Request):
    kinde_client = KindeApiClient(**kinde_api_client_params)
    login_url = kinde_client.get_login_url()
    return RedirectResponse(login_url)


# Register endpoint
@app.get("/api/auth/register")
def register(request: Request):
    kinde_client = KindeApiClient(**kinde_api_client_params)
    register_url = kinde_client.get_register_url()
    return RedirectResponse(register_url)


@app.get("/api/auth/kinde_callback")
def callback(request: Request):
    kinde_client = KindeApiClient(**kinde_api_client_params)
    kinde_client.fetch_token(authorization_response=str(request.url))
    user = kinde_client.get_user_details()
    request.session["user_id"] = user.get("id")
    user_clients[user.get("id")] = kinde_client
    return RedirectResponse(router.url_path_for("read_root"))


# Logout endpoint
@app.get("/api/auth/logout")
def logout(request: Request):
    user_id = request.session.get("user_id")
    if user_id in user_clients:
        kinde_client = user_clients[user_id]
        logout_url = kinde_client.logout(redirect_to=config.LOGOUT_REDIRECT_URL)
        del user_clients[user_id]
        request.session.pop("user_id", None)
        return RedirectResponse(logout_url)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


app.include_router(router)
