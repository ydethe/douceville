import os

from pydantic_settings import BaseSettings, SettingsConfigDict


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    LOGIN_DISABLED: bool

    LOGFIRE_TOKEN: str
    LOGLEVEL: str
    FLASK_ADMIN_SWATCH: str
    BCRYPT_ROUNDS: int
    OPENROUTESERVICE_KEY: str
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str

    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USE_TLS: bool
    MAIL_USE_SSL: bool
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_DEFAULT_SENDER: str

    POSTGRES_HOST: str
    ADDOK_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    HOST: str
    PROTOCOL: str
    API_PATH: str
    PRICE_ID: str

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
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"


config = Config()
