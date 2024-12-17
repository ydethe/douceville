import os

from pydantic_settings import BaseSettings, SettingsConfigDict


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    LOGFIRE_TOKEN: str
    LOGLEVEL: str
    OPENROUTESERVICE_KEY: str

    ADDOK_HOST: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    API_PATH: str

    # https://supabase.com/docs/reference/python/initializing
    # https://github.com/orgs/supabase/discussions/226#discussioncomment-89148
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_TEST_USER: str
    SUPABASE_TEST_PASSWORD: str
    SUPABASE_JWT_SECRET: str
    SUPABASE_ADMIN_KEY: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.POSTGRES_HOST == "<test>":
            db_uri = "sqlite:///tests/test.db"
            init_sqlite(db_uri)
            return db_uri
        else:
            return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"


def init_sqlite(db_uri: str):
    from geoalchemy2 import load_spatialite
    from sqlalchemy import create_engine, select
    from sqlalchemy.event import listen
    from sqlalchemy.orm import Session
    from douceville.schemas import Etablissement, Resultat
    import os

    os.environ["SPATIALITE_LIBRARY_PATH"] = "/usr/lib/x86_64-linux-gnu/mod_spatialite.so"
    engine = create_engine(db_uri, echo=True)
    listen(engine, "connect", load_spatialite)
    with Session(engine) as session:
        stmt = select(Etablissement)
        nb_found = len(list(session.scalars(stmt)))
        if nb_found == 0:
            etab = Etablissement(
                id=1,
                UAI="X42Y",
                nom="FooBar school",
                code_postal="31000",
                commune="Toulouse",
                position="POINT(1 32)",
                departement="31",
                secteur="public",
                nature="lycée",
            )
            session.add_all([etab])
            session.commit()

        stmt = select(Resultat)
        nb_found = len(list(session.scalars(stmt)))
        if nb_found == 0:
            resultat = Resultat(id=1, diplome="Brevet", annee=2024, etablissement_uai="X42Y")
            session.add_all([resultat])
            session.commit()


config = Config()
