import json
import pickle
import time
import argparse

import tqdm
from rdflib import Graph

from douceville.utils import logged
from douceville.scripts.read_config import loadConfig


@logged
def create_cache(logger=None):
    # src : CollegesLycees/raw/dataset-564055.ttl
    # dst : CollegesLycees/raw/data_dict.raw

    parser = argparse.ArgumentParser(description="Conversion rdf")
    parser.add_argument("cfg", help="fichier config", type=str)
    parser.add_argument("src", help="fichier in", type=str)

    args = parser.parse_args()
    cfg = args.cfg
    src = args.src

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
    create_cache()


if __name__ == "__main__":
    conv_rdf_main()
