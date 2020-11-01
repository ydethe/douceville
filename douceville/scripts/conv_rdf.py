import json
import pickle
import time
import argparse

import tqdm
from rdflib import Graph

from douceville.utils import logged
from douceville.scripts.read_config import loadConfig


@logged
def create_cache(cfg, src, logger=None):
    logger.info(time.ctime(), "Creating geoloc cache 'data_dict.raw'...")

    c = loadConfig(cfg)
    dst = c.geoloc2

    if dst is None:
        logger.error("No geoloc file specified in %s" % cfg)
    elif dst == src:
        logger.error("Same source and destination %s" % src)
    else:
        g = Graph()
        g.parse(src, format="n3")

        raw = g.serialize(format="json-ld").decode("utf-8")

        info = json.loads(raw)

        pickle.dump(info, open(dst, "wb"))

    logger.info(time.ctime(), "Done.")


def import_geoloc_db(fic):
    info = pickle.loads(open(fic, "rb").read())

    db = {}
    for rec in tqdm.tqdm(info):
        if not "@id" in rec.keys():
            continue

        uai = rec["@id"].split("/")[-1].upper()

        if uai in db.keys():
            dat = db[uai]
        else:
            dat = {"UAI": uai}

        if "/geometry/" in rec["@id"]:
            lon = rec["http://data.ign.fr/ontologies/geometrie#coordX"][0]["@value"]
            lat = rec["http://data.ign.fr/ontologies/geometrie#coordY"][0]["@value"]

            dat["latitude"] = lat
            dat["longitude"] = lon

        if "http://purl.org/dc/terms/title" in rec.keys():
            nom = rec["http://purl.org/dc/terms/title"][0]["@value"]
            dat["nom"] = nom

        if (
            "http://data.eurecom.fr/ontologies/ecole#denominationPrincipale"
            in rec.keys()
        ):
            denom = rec[
                "http://data.eurecom.fr/ontologies/ecole#denominationPrincipale"
            ][0]["@value"]
            dat["denomination"] = denom

        db[uai] = dat

    db["0312843X"] = {"UAI": "0312843X", "longitude": 1.398089, "latitude": 43.464582}
    db["0312868Z"] = {"UAI": "0312868Z", "longitude": 1.249387, "latitude": 43.348657}
    db["0312842W"] = {"UAI": "0312842W", "longitude": 1.373549, "latitude": 43.750734}
    db["0311842J"] = {"UAI": "0311842J", "longitude": 1.579625, "latitude": 43.728851}
    db["0312354R"] = {"UAI": "0312354R", "longitude": 1.320462, "latitude": 43.780609}
    db["0311270M"] = {"UAI": "0311270M", "longitude": 1.522781, "latitude": 43.537348}
    db["0311843K"] = {"UAI": "0311843K", "longitude": 1.120444, "latitude": 43.413620}
    db["0311268K"] = {"UAI": "0311268K", "longitude": 0.730726, "latitude": 43.117691}
    db["0312058U"] = {"UAI": "0312058U", "longitude": 0.952023, "latitude": 43.081886}
    db["0310087B"] = {"UAI": "0310087B", "longitude": 1.474957, "latitude": 43.549452}
    db["0311879Z"] = {"UAI": "0311879Z", "longitude": 1.551114, "latitude": 43.473410}

    return db


def conv_rdf_main():
    # src : CollegesLycees/raw/dataset-564055.ttl
    # dst : CollegesLycees/raw/data_dict.raw

    parser = argparse.ArgumentParser(description="Conversion rdf")
    parser.add_argument("cfg", help="fichier config", type=str)
    parser.add_argument("src", help="fichier in", type=str)

    args = parser.parse_args()

    create_cache(args.cfg, args.src)


if __name__ == "__main__":
    conv_rdf_main()
