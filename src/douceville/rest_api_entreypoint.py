import typing as T

import logfire
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlmodel import select

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
from .auth import get_token_user


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
router = APIRouter()

logfire.instrument_fastapi(app)


@router.get("/etablissement/{uai}", response_model=EtablissementPublicAvecResultats)
async def read_etablissement(
    uai: str,
    kinde_client: DvUser = Depends(get_token_user),
    db: Session = Depends(get_db),
) -> EtablissementPublicAvecResultats:
    etab = get_etab(db, uai)
    # TODO: Handle the case where no etablissement is found. Return NOT FOUND error
    return etab


@router.post("/etablissements", response_model=T.List[EtablissementPublicAvecResultats])
async def etablissement_in_zone(
    body: QueryParameters,
    kinde_client: DvUser = Depends(get_token_user),
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
    kinde_client: DvUser = Depends(get_token_user),
) -> Isochrone:
    center = [lon, lat]
    iso = calcIsochrone(center, dist, transp)

    return iso


@router.get("/user", response_model=DvUser)
async def get_user(
    user: DvUser = Depends(get_token_user),
) -> DvUser:
    return user


app.include_router(router)
