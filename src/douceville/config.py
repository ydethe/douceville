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
    SECRET_KEY: str
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
    PORT: int
    PROTOCOL: str
    PRICE_ID: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"


config = Config()
