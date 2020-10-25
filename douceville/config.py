import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://web_user@localhost/maillage"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "etablissements.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "https://douceville.fr"
    PORT = 443
    SECRET_KEY = "ITSASECRET"
