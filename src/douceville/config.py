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
        db_uri = f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"
        if self.POSTGRES_HOST == "localhost":
            init_test_db(db_uri)
        return db_uri


def init_test_db(db_uri: str):
    from sqlmodel import Session, create_engine, select, SQLModel
    from douceville.schemas import Etablissement, Resultat

    engine = create_engine(db_uri, echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        stmt = select(Etablissement).where(Etablissement.UAI == "X42Y")
        nb_found = len(list(session.scalars(stmt)))
        if nb_found == 0:
            etab = Etablissement(
                id=1,
                UAI="X42Y",
                nom="FooBar Test School",
                code_postal="31000",
                commune="Toulouse",
                position="POINT(2 45)",
                departement="31",
                secteur="public",
                nature="lycée",
            )
            session.add_all([etab])
            session.commit()

        stmt = select(Resultat).where(Resultat.etablissement_uai == "X42Y")
        nb_found = len(list(session.scalars(stmt)))
        if nb_found == 0:
            resultat = Resultat(id=1, diplome="Brevet", annee=2024, etablissement_uai="X42Y")
            session.add_all([resultat])
            session.commit()


config = Config()
