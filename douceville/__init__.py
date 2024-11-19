"""
   Manipulation of algebraic numbers
   Y. de The
"""

import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler

from .config import config

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger("douceville_logger")
logger.setLevel(config.LOGLEVEL.upper())

stream_handler = RichHandler()
logger.addHandler(stream_handler)

file_handler = RotatingFileHandler("douceville.log", maxBytes=10e6, backupCount=5)
logger.addHandler(file_handler)
