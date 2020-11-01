import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = b"lVwBk7UXvvhDlURHQ7iBnyFy-PBvBrUhHQ5NsDlcRh0="
    OPENROUTESERVICE_KEY = "5b3ce3597851110001cf6248b3fbd66e5be24021b1ea77cb39f76783"
    FLASK_ADMIN_SWATCH = "cerulean"


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://web_user@localhost/douceville"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "https://douceville.fr"
    PORT = 443


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/mydb.db" % basedir
    SQLITE_SPATIALITE_PATH = "/usr/local/lib/mod_spatialite.so"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    HOST = "https://localhost"
    PORT = 5000


class Dev2Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://cl_user@localhost/douceville"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    HOST = "https://localhost"
    PORT = 5000


Config = Dev2Config
# Config = ProdConfig
