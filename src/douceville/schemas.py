import typing as T
from datetime import datetime
import json

from pydantic import field_validator, BaseModel
import sqlalchemy as sa
from geoalchemy2 import Geometry, WKBElement
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, UniqueConstraint, Column

from .config import config


# ==============================
# Database access
# ==============================
def get_engine():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
    SQLModel.metadata.create_all(engine)

    return engine


def get_db():
    engine = get_engine()

    with Session(engine) as session:
        yield session


def create_db_and_tables():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
    SQLModel.metadata.create_all(engine)


# ==============================
# Authentication objects
# ==============================
class Url(BaseModel):
    url: str


class AuthorizationResponse(BaseModel):
    state: str
    code: str


class DvUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    login: str = Field(nullable=False, unique=True)
    name: str = Field(nullable=True, unique=False)
    company: str = Field(nullable=True, unique=False)
    location: str = Field(nullable=True, unique=False)
    email: str = Field(nullable=True, unique=True)
    avatar_url: str = Field(nullable=True, unique=False)
    hashed_pwd: str = Field(nullable=True)
    admin: bool = Field(nullable=False, default=False)
    active: bool = Field(nullable=False, default=False)


class GithubUser(BaseModel):
    login: str
    name: str
    company: T.Optional[str]
    location: T.Optional[str]
    email: T.Optional[str]
    avatar_url: T.Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str
    user: DvUser


# ==============================
# Etablissement objects
# ==============================
class EtablissementBase(SQLModel):
    UAI: str = Field(nullable=False, unique=True)
    nom: str = Field(nullable=False)
    adresse: T.Optional[str] = Field(nullable=True)
    lieu_dit: T.Optional[str] = Field(nullable=True)
    code_postal: str = Field(nullable=False)
    commune: str = Field(nullable=False)
    position: T.Any = Field(sa_column=Column(Geometry("POINT"), nullable=False))
    departement: str = Field(nullable=False)
    academie: T.Optional[str] = Field(nullable=True)
    secteur: str = Field(nullable=False)
    ouverture: T.Optional[datetime] = Field(nullable=True)
    nature: str = Field(nullable=False)

    @field_validator("position", mode="before")
    def convert_geom_to_geojson(cls, v):
        if v is None:
            # Probably unnecessary if field is not nullable
            return None
        elif isinstance(v, WKBElement):
            # e.g. session.get results in a `WKBElement`
            v = sa.func.ST_AsGeoJSON(v)
        elif isinstance(v, sa.func.ST_AsGeoJSON):
            # e.g. session.exec(select(Aoi)).all() gives v as an instance of sa.func.ST_AsGeoJSON
            pass
        else:
            raise ValueError(f"Received unexpected type: {type(v)}")

        # Convert sa.func.ST_AsGeoJSON to json, which geojson-pydantic can then ingest
        engine = get_engine()
        with Session(engine) as session:
            return json.loads(session.scalar(v))


class Etablissement(EtablissementBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    resultats: list["Resultat"] = Relationship(back_populates="etablissement", cascade_delete=True)


class EtablissementCreate(EtablissementBase):
    pass


class EtablissementPublic(EtablissementBase):
    id: int


class EtablissementUpdate(SQLModel):
    UAI: str | None = None
    nom: str | None = None
    adresse: str | None = None
    lieu_dit: str | None = None
    code_postal: str | None = None
    commune: str | None = None
    position: T.Any | None = None
    departement: str | None = None
    academie: str | None = None
    secteur: str | None = None
    ouverture: datetime | None = None
    nature: str | None = None


# ==============================
# Resultats objects
# ==============================
class ResultatBase(SQLModel):
    diplome: str = Field(nullable=False)
    annee: int = Field(nullable=False)
    presents: T.Optional[int] = Field(nullable=True)
    admis: T.Optional[int] = Field(nullable=True)
    mentions: T.Optional[int] = Field(nullable=True)
    etablissement_uai: str | None = Field(
        default=None, foreign_key="etablissement.UAI", ondelete="CASCADE"
    )


class Resultat(ResultatBase, table=True):
    __table_args__ = (UniqueConstraint("diplome", "annee", "etablissement_uai"),)

    idx: int | None = Field(default=None, primary_key=True)
    etablissement: Etablissement | None = Relationship(back_populates="resultats")


class ResultatPublic(ResultatBase):
    id: int


class ResultatCreate(ResultatBase):
    pass


class ResultatUpdate(SQLModel):
    diplome: str | None = None
    annee: int | None = None
    presents: int | None = None
    admis: int | None = None
    mentions: int | None = None
    etablissement_uai: str | None = None


class ResultatPublicAvecEtablissement(ResultatPublic):
    etablissement: EtablissementPublic | None = None


class EtablissementPublicAvecResultats(EtablissementPublic):
    resultats: list[Resultat] = []
