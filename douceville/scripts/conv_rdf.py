import json
import logging
from pathlib import Path
import pickle
import time

import typer
from rdflib import Graph, plugin
from rdflib.serializer import Serializer

from douceville.scripts.read_config import loadConfig


app = typer.Typer()


@app.command()
def create_cache(
    cfg: Path = typer.Argument(..., help="Fichier de config"),
    src: Path = typer.Argument(..., help="Fichier .ttl"),
):
    logger = logging.getLogger("douceville_logger")
    # src : CollegesLycees/raw/dataset-564055.ttl
    # dst : CollegesLycees/raw/data_dict.raw

    logger.info("[%s]Creating geoloc cache 'data_dict.raw'..." % time.ctime())

    c = loadConfig(cfg)
    dst = c.geoloc2

    if dst is None:
        logger.error("No geoloc file specified in %s" % cfg)
    elif dst == src:
        logger.error("Same source and destination %s" % src)
    else:
        g = Graph()
        g.parse(src, format="n3")

        raw = g.serialize(format="json-ld")

        info = json.loads(raw)

        pickle.dump(info, open(dst, "wb"))

    logger.info("[%s]Done." % time.ctime())


def conv_rdf_main():
    app()
