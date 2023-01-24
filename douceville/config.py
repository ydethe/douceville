import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ADMIN_SWATCH = "cerulean"
    BCRYPT_ROUNDS = 10
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        None,
    )
    OPENROUTESERVICE_KEY = os.environ.get(
        "OPENROUTESERVICE_KEY",
        None,
    )
    STRIPE_SECRET_KEY = os.environ.get(
        "STRIPE_SECRET_KEY",
        None,
    )
    STRIPE_PUBLISHABLE_KEY = os.environ.get(
        "STRIPE_PUBLISHABLE_KEY",
        None,
    )

    MAIL_SERVER = os.environ.get("MAIL_SERVER", None)
    MAIL_PORT = os.environ.get("MAIL_PORT", None)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", None)
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", None)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", None)
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", None)
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", None)

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", None)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", None)
    HOST = os.environ.get("HOST", None)
    PORT = os.environ.get("PORT", None)
    PRICE_ID = os.environ.get("PRICE_ID", None)
    DEBUG = os.environ.get("DEBUG", None)
