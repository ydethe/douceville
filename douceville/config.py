import os

from cryptography.fernet import Fernet


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    FLASK_ADMIN_SWATCH = "cerulean"
    BCRYPT_ROUNDS = 10
    # SECRET_KEY = Fernet.generate_key()
    SECRET_KEY = "VLt1XfxWyYcHcIZm92vcDAeoOUWqSQgx3_Mq8c7CCKE="
    OPENROUTESERVICE_KEY = os.environ.get(
        "OPENROUTESERVICE_KEY",
        "5b3ce3597851110001cf6248f1d3b3fb5b69489b954df2b1842b88d7",
    )
    STRIPE_SECRET_KEY = os.environ.get(
        "STRIPE_SECRET_KEY",
        "sk_test_51HlJlVGFonhtEiXEelNtjMjZL6WjoUNqT2pSvGo6n71DjzHq2E9QCzgEgF310xHFrcs4ucp4po2Hc0H4TBpmp3vn00JnZPpkrL",
    )
    STRIPE_PUBLISHABLE_KEY = os.environ.get(
        "STRIPE_PUBLISHABLE_KEY",
        "pk_test_51HlJlVGFonhtEiXEqSa9aIeqpQis9hpyiHEtDbrZUnnDInKdxZzBLxxZAre5bTh5qntfqwzloQriY0PCCeURxten00QB0hoezk",
    )

    MAIL_SERVER = "box.johncloud.fr"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "yann@johncloud.fr"
    MAIL_PASSWORD = "c86WHgSpo6hdPj"
    MAIL_DEFAULT_SENDER = ("Yann", "yann@johncloud.fr")


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://douceville:douceville@db/douceville"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "https://douceville.fr"
    PORT = 443
    PRICE_ID = "price_1HoCr3GFonhtEiXEAgLKb9WD"


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/mydb.db" % basedir
    SQLITE_SPATIALITE_PATH = "/usr/local/lib/mod_spatialite.so"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    HOST = "https://localhost"
    PORT = 5000
    PRICE_ID = "price_1HmzS4GFonhtEiXEjsWOdekb"


class Dev2Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://douceville:douceville@localhost/douceville"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    HOST = "https://localhost"
    PORT = 5000
    PRICE_ID = "price_1HmzS4GFonhtEiXEjsWOdekb"


tgt_conf = os.environ.get("DOUCEVILLE_CONFIG", "dev")
if tgt_conf == "prod":
    Config = ProdConfig
else:
    Config = Dev2Config
