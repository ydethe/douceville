import os


basedir = os.path.abspath(os.path.dirname(__file__))


class ProdConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://web_user@localhost/douceville"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "https://douceville.fr"
    PORT = 443
    SECRET_KEY = b"lVwBk7UXvvhDlURHQ7iBnyFy-PBvBrUhHQ5NsDlcRh0="


class DevConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/mydb.db" % basedir
    SQLITE_SPATIALITE_PATH = "/usr/local/lib/mod_spatialite.so"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    HOST = "https://localhost"
    PORT = 5000
    SECRET_KEY = b"lVwBk7UXvvhDlURHQ7iBnyFy-PBvBrUhHQ5NsDlcRh0="


class Dev2Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://cl_user@localhost/douceville"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    HOST = "https://localhost"
    PORT = 5000
    SECRET_KEY = b"lVwBk7UXvvhDlURHQ7iBnyFy-PBvBrUhHQ5NsDlcRh0="


Config = ProdConfig
