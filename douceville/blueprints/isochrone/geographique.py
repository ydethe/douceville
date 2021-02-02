from collections import defaultdict

from openrouteservice import client, geocode

from douceville.config import Config
from douceville.utils import logged


def calcIsochrone(center, dist, transp):
    # https://openrouteservice.org/dev/#/home?tab=1
    api_key = Config.OPENROUTESERVICE_KEY
    clnt = client.Client(key=api_key)

    # Request of isochrones with 15 minute footwalk.
    params_iso = {
        "profile": transp,
        "intervals": [dist],  # time in seconds
        "segments": dist,
        "attributes": ["total_pop"],  # Get population count for isochrones
        "locations": [center],
    }

    iso = clnt.isochrones(**params_iso)  # Perform isochrone request

    return iso


@logged
def geocodeUserAddress(query, logger=None):
    api_key = Config.OPENROUTESERVICE_KEY
    clnt = client.Client(key=api_key)

    lon = lat = None
    j = geocode.pelias_search(
        clnt,
        query,
        country="FR",
        layers=["postalcode", "address", "locality", "venue"],
    )
    for f in j["features"]:
        lon, lat = f["geometry"]["coordinates"]

        return lon, lat


@logged
def findCoordFromAddress(
    nom=None, adresse=None, cp=None, commune=None, lat=None, lon=None, logger=None
):
    """

    Examples:
    >>> findCoordFromAddress(nom='Lycee Henri Matisse',cp='31270',commune='Cugnaux')
    (1.352366, 43.530729)
    >>> # findCoordFromAddress(nom='Cours Des Frères Montgolfier',adresse='12 Place Georges Pompidou',cp='93165',commune='Noisy-Le-Grand')
    # (2.551383, 48.838077)
    >>> # findCoordFromAddress(nom='Ecole Alternative Du Pays De Gex',adresse='Place',cp='1280',commune='Préssin-Moëns')
    # (2.551383, 48.838077)

    """
    etab_maj = defaultdict(lambda: None)

    api_key = Config.OPENROUTESERVICE_KEY
    clnt = client.Client(key=api_key)

    def geocode_query(
        clnt, nom=None, adresse=None, cp=None, commune=None, lat=None, lon=None
    ):
        query = ""
        if not nom is None:
            query += nom + ","
        if not adresse is None:
            etab_maj["adresse"] = adresse
            query += adresse + ","
        if not cp is None:
            etab_maj["code_postal"] = cp
            query += cp + ","
        if not commune is None:
            etab_maj["commune"] = commune
            query += commune + ","
        else:
            logger.error("In findCoordFromAddress, argument 'commune' must not be None")
            return None, None

        lon = lat = None
        j = geocode.pelias_search(
            clnt,
            query,
            country="FR",
            layers=["postalcode", "address", "locality", "venue"],
        )
        for f in j["features"]:
            if not "locality" in f["properties"].keys():
                continue

            if (
                len(j["features"]) == 1
                or f["properties"]["locality"].lower() == commune.lower()
            ):
                lon, lat = f["geometry"]["coordinates"]

        return lon, lat

    if lat is None or lon is None:
        lon, lat = geocode_query(clnt, nom, adresse, cp, commune)

    if lat is None and not adresse is None:
        lon, lat = geocode_query(clnt, nom=nom, adresse=None, cp=cp, commune=commune)

    if lat is None and not nom is None:
        lon, lat = geocode_query(clnt, nom=None, adresse=None, cp=cp, commune=commune)

    if lat is None and not cp is None:
        lon, lat = geocode_query(clnt, nom=None, adresse=None, cp=None, commune=commune)

    if lat is None:
        logger.error("geoloc failed : %s, %s, %s, %s" % (nom, adresse, cp, commune))
        return None

    if nom is None or adresse is None or cp is None:
        j = geocode.pelias_reverse(clnt, [lon, lat], country="FR")
        for f in j["features"]:
            p = f["properties"]
            if "postalcode" in p.keys() and "name" in p.keys():
                adresse = p["name"]
                cp = p["postalcode"].zfill(5)

    etab_maj["position"] = "POINT(%f %f)" % (lon, lat)
    etab_maj["commune"] = commune
    etab_maj["code_postal"] = cp
    etab_maj["adresse"] = adresse
    etab_maj["departement"] = cp[:2]

    return etab_maj


if __name__ == "__main__":
    import doctest

    doctest.testmod()
