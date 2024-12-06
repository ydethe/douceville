import typing as T
from datetime import datetime

from pydantic import BaseModel
from geoalchemy2 import Geometry
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, UniqueConstraint, Column

from .config import config


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


class Etablissement(SQLModel, table=True):
    UAI: str | None = Field(default=None, primary_key=True)
    nom: str = Field(nullable=False)
    adresse: str = Field(nullable=True)
    lieu_dit: str = Field(nullable=True)
    code_postal: str = Field(nullable=False)
    commune: str = Field(nullable=False)
    # https://gist.github.com/joshuapowell/e209a4dac5c8187ea8ce#file-gistfile1-md
    position: T.Any = Field(sa_column=Column(Geometry("POINT"), nullable=False))
    departement: str = Field(nullable=False)
    academie: str = Field(nullable=True)
    secteur: str = Field(nullable=False)
    ouverture: datetime = Field(nullable=True)
    nature: str = Field(nullable=False)

    resultats: list["Resultat"] = Relationship(back_populates="etablissement", cascade_delete=True)


class Resultat(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("diplome", "annee", "etablissement_uai"),)

    idx: int | None = Field(default=None, primary_key=True)
    diplome: str = Field(nullable=False)
    annee: int = Field(nullable=False)
    presents: int = Field(nullable=True)
    admis: int = Field(nullable=True)
    mentions: int = Field(nullable=True)
    etablissement_uai: str | None = Field(
        default=None, foreign_key="etablissement.UAI", ondelete="CASCADE"
    )
    etablissement: Etablissement | None = Relationship(back_populates="resultats")


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
