"""

.. include:: ../../README.md

# CLI usage

douceville comes with a CLI tool called dv-cli.

# Testing

## Run the tests

To run tests, just run:

    pdm run pytest

## Test reports

[See test report](../tests/report.html)

[See coverage](../coverage/index.html)

.. include:: ../../CHANGELOG.md

"""


import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import logfire
from rich.logging import RichHandler

from .config import config


# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger("douceville_logger")
logger.setLevel(config.LOGLEVEL.upper())

logfire.configure(token=config.LOGFIRE_TOKEN, console=False)

log_pth = Path("logs")
if not log_pth.exists():
    log_pth.mkdir(exist_ok=True)
file_handler = RotatingFileHandler("logs/douceville.log", maxBytes=10e6, backupCount=5)
term_handler = RichHandler(rich_tracebacks=False)
lf_handler = logfire.LogfireLoggingHandler(fallback=term_handler)

logger.addHandler(file_handler)
logger.addHandler(lf_handler)
logger.addHandler(term_handler)
