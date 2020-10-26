"""
   Manipulation of algebraic numbers
   Y. de The
"""
from pkg_resources import get_distribution
import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from douceville.config import Config


try:
    __version__ = get_distribution(__name__).version
except Exception as e:
    __version__ = "dev"

__author__ = "Y. de The"
__email__ = "yann@johncloud.fr"


# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger("collegeslycees_logger")
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)

# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter("[%(levelname)s]%(message)s")
# création d'un handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# os.makedirs("logs", exist_ok=True)

# now = datetime.now()
# sd = now.strftime("%Y_%m_%d_%H_%M_%S")
file_handler = logging.FileHandler(
"douceville.log", mode="w", encoding="utf-8", delay=False
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# create and configure the app
# app = Flask(__name__, instance_relative_config=True, static_url_path='static')
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev",
)
app.config.from_object(Config)
app.logger.addHandler(file_handler)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from douceville import routes, models

