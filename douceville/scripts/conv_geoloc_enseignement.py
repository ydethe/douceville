import json
import logging
from pathlib import Path
import pickle
import time

import typer
import pandas as pd
from rdflib import Graph

from douceville.scripts.read_config import loadConfig


app = typer.Typer()


@app.command()
def create_cache(
    cfg: Path = typer.Argument(..., help="Fichier de config"),
    src: Path = typer.Argument(..., help="Fichier .xlsx"),
):
    """Conversion rdf"""
    logger = logging.getLogger("douceville_logger")
    logger.info("Creating geoloc cache '%s'..." % src)

    c = loadConfig(cfg)
    dst = c.geoloc

    if dst is None:
        logger.error("No geoloc file specified in %s" % cfg)
    elif dst == src:
        logger.error("Same source and destination %s" % src)
    else:
        df = pd.read_excel(src)
        df.to_pickle(dst)

    logger.info("Done.")


def import_geoloc_db(fic):
    df = pd.read_pickle(fic)

    # db["0312843X"] = {"UAI": "0312843X", "longitude": 1.398089, "latitude": 43.464582}
    # db["0312868Z"] = {"UAI": "0312868Z", "longitude": 1.249387, "latitude": 43.348657}
    # db["0312842W"] = {"UAI": "0312842W", "longitude": 1.373549, "latitude": 43.750734}
    # db["0311842J"] = {"UAI": "0311842J", "longitude": 1.579625, "latitude": 43.728851}
    # db["0312354R"] = {"UAI": "0312354R", "longitude": 1.320462, "latitude": 43.780609}
    # db["0311270M"] = {"UAI": "0311270M", "longitude": 1.522781, "latitude": 43.537348}
    # db["0311843K"] = {"UAI": "0311843K", "longitude": 1.120444, "latitude": 43.413620}
    # db["0311268K"] = {"UAI": "0311268K", "longitude": 0.730726, "latitude": 43.117691}
    # db["0312058U"] = {"UAI": "0312058U", "longitude": 0.952023, "latitude": 43.081886}
    # db["0310087B"] = {"UAI": "0310087B", "longitude": 1.474957, "latitude": 43.549452}
    # db["0311879Z"] = {"UAI": "0311879Z", "longitude": 1.551114, "latitude": 43.473410}

    return df


def conv_geoloc_enseignement_main():
    app()
