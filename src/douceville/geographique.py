from pathlib import Path
import pickle
import time
import typing as T

import requests
from openrouteservice import client, geocode

from .config import config
from .schemas import Isochrone
from . import logger


def calcIsochrone(
    lonlat: T.Tuple[float, float],
    dist: float,
    transp: T.Literal[
        "driving-car",
        "driving-hgv",
        "foot-walking",
        "foot-hiking",
        "cycling-regular",
        "cycling-road",
        "cycling-mountain",
        "cycling-electric",
    ],
) -> Isochrone:
    # https://openrouteservice.org/dev/#/home?tab=1
    api_key = config.OPENROUTESERVICE_KEY
    clnt = client.Client(key=api_key)

    params_iso = {
        "profile": transp,
        "range": [dist],  # time in seconds
        "interval": dist,
        "attributes": [],  # Get population count for isochrones
        "locations": [lonlat],
    }

    res = clnt.isochrones(**params_iso)  # Perform isochrone request
    time.sleep(1)  # To comply with rate limiting

    iso = Isochrone(
        lonlat=lonlat,
        dist=dist,
        transp=transp,
        geometry=res["features"][0]["geometry"]["coordinates"][0],
    )

    return iso


def geocodeUserAddress(query):
    api_key = config.OPENROUTESERVICE_KEY
    clnt = client.Client(key=api_key)

    lon = lat = None
    j = geocode.pelias_search(
        clnt,
        query,
        size=50,
        country="FR",
        layers=["postalcode", "address", "locality", "venue"],
    )
    time.sleep(1)  # To comply with rate limiting
    for f in j["features"]:
        lon, lat = f["geometry"]["coordinates"]

        return lon, lat


def geocode_query(
    clnt,
    etab_maj: dict,
    nom=None,
    adresse=None,
    departement=None,
    cp: str = None,
    commune=None,
    lat=None,
    lon=None,
):
    queryl = []

    if nom is not None and adresse is None:
        query_name = nom.lower()
        if "collège" in query_name:
            query_name = query_name.replace("collège", "")
        if "college" in query_name:
            query_name = query_name.replace("college", "")
        if "privé" in query_name:
            query_name = query_name.replace("privé", "")
        if "prive" in query_name:
            query_name = query_name.replace("prive", "")
        if "lycée" in query_name:
            query_name = query_name.replace("lycée", "")
        if "lycee" in query_name:
            query_name = query_name.replace("lycee", "")
        if "public" in query_name:
            query_name = query_name.replace("public", "")
        if "hors contrat" in query_name:
            query_name = query_name.replace("hors contrat", "")
        if "professionnel" in query_name:
            query_name = query_name.replace("professionnel", "")
        queryl.append(query_name)

    if adresse is not None:
        etab_maj["adresse"] = adresse
        queryl.append(adresse)

    # if cp is not None:
    #     etab_maj["code_postal"] = cp
    #     queryl.append(cp)

    if commune is not None:
        etab_maj["commune"] = commune
        queryl.append(commune)
    else:
        logger.error("In findCoordFromAddress, argument 'commune' must not be None")
        return None, None

    if departement is not None:
        etab_maj["departement"] = departement
        queryl.append(departement)

    queryl.append("France")

    query = ", ".join(queryl)

    lon = lat = None

    url = "https://photon.komoot.io/api/?q={query}"
    res = requests.get(url.format(query=query))
    j = res.json()

    # j = geocode.pelias_search(
    #     clnt,
    #     rect_max_y=rect_max_y,
    #     text=query,
    #     size=10,
    # )
    time.sleep(1)  # To comply with rate limiting

    if len(j["features"]) > 0:
        found_feat = j["features"][0]
        lon, lat = found_feat["geometry"]["coordinates"]
        # Il arrive que le geocoder n'arrive pas à positionner un établissement
        # calédonien : la latitude renvoyée est positive. On considère donc que dans ce cas,
        # l'établissement n'a pas pu être positionné
        if cp.startswith("98") and lat > 0:
            lon = None
            lat = None

    return lon, lat


def findCoordFromAddress(
    nom: str = None,
    adresse: str = None,
    departement: str = None,
    cp: str = None,
    commune: str = None,
    lat: float = None,
    lon: float = None,
) -> dict:
    """
    pyth
        Examples:
        >>> res=findCoordFromAddress(nom='Lycee Henri Matisse',cp='31270',commune='Cugnaux')
        >>> res['latitude']
        43.5313895
        >>> # findCoordFromAddress(nom='Cours Des Frères Montgolfier',adresse='12 Place Georges Pompidou',cp='93165',commune='Noisy-Le-Grand')
        # (2.551383, 48.838077)
        >>> # findCoordFromAddress(nom='Ecole Alternative Du Pays De Gex',adresse='Place',cp='1280',commune='Préssin-Moëns')
        # (2.551383, 48.838077)

    """
    cache_pth = Path(".cache")
    if not cache_pth.exists():
        with open(cache_pth, "wb") as cache_fd:
            pickle.dump({}, cache_fd)

    cache_fd = open(cache_pth, "rb")
    data = pickle.load(cache_fd)
    key = (nom, adresse, departement, cp, commune, lat, lon)
    if key in data.keys():
        res = data[key]
        if "position" in res.keys() and "latitude" in res.keys() and "longitude" in res.keys():
            if (
                res["position"] is not None
                and res["latitude"] is not None
                and res["longitude"] is not None
            ):
                if not cp.startswith("98") or res["latitude"] < 0:
                    return res

    etab_maj = dict(
        position=None,
        commune=None,
        departement=None,
        code_postal=None,
        adresse=None,
    )

    clnt = client.Client(key=config.OPENROUTESERVICE_KEY)

    if lat is None or lon is None:
        lon, lat = geocode_query(clnt, etab_maj, nom, adresse, departement, cp, commune)

    if (nom is None or adresse is None or cp is None) and lon is not None and lat is not None:
        j = geocode.pelias_reverse(clnt, [lon, lat], country="FR")
        time.sleep(1)  # To comply with rate limiting

        for f in j["features"]:
            p = f["properties"]
            if "postalcode" in p.keys() and "name" in p.keys():
                adresse = p["name"]
                cp = p["postalcode"].zfill(5)

    if lon is not None and lat is not None:
        etab_maj["position"] = "POINT(%f %f)" % (lon, lat)
    etab_maj["commune"] = commune
    etab_maj["code_postal"] = cp
    etab_maj["adresse"] = adresse
    etab_maj["departement"] = cp[:2]
    etab_maj["latitude"] = lat
    etab_maj["longitude"] = lon

    if etab_maj["position"] is not None:
        data[key] = etab_maj
    cache_fd.close()

    with open(cache_pth, "wb") as cache_fd:
        pickle.dump(data, cache_fd)

    return etab_maj
