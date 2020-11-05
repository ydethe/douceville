from openrouteservice import client, geocode

from douceville.config import Config
from douceville.utils import logged


def calcIsochrone(center, dist):
    # https://openrouteservice.org/dev/#/home?tab=1
    api_key = Config.OPENROUTESERVICE_KEY
    clnt = client.Client(key=api_key)

    # Request of isochrones with 15 minute footwalk.
    params_iso = {
        "profile": "driving-car",
        "intervals": [dist],  # time in seconds
        "segments": dist,
        "attributes": ["total_pop"],  # Get population count for isochrones
        "locations": [center],
    }

    iso = clnt.isochrones(**params_iso)  # Perform isochrone request

    return iso

@logged
def findCoordFromAddress(nom=None,adresse=None,cp=None,commune=None, logger=None):
    '''

    Examples:
    >>> findCoordFromAddress(nom='Lycee Henri Matisse',cp='31270',commune='Cugnaux')
    (1.352366, 43.530729)
    >>> findCoordFromAddress(nom='Cours Des Frères Montgolfier',adresse='12 Place Georges Pompidou',cp='93165',commune='Noisy-Le-Grand')
    (2.551383, 48.838077)
    >>> findCoordFromAddress(nom='Ecole Alternative Du Pays De Gex',adresse='Place',cp='1280',commune='Préssin-Moëns')
    (2.551383, 48.838077)

    '''
    query = ''
    if not nom is None:
        query += nom + ','
    if not adresse is None:
        query += adresse + ','
    if not cp is None:
        query += cp + ','
    if not commune is None:
        query += commune + ','
    query += 'France'
    
    api_key = Config.OPENROUTESERVICE_KEY
    clnt = client.Client(key=api_key)

    lat = None
    lon = None
    j = geocode.pelias_search(clnt, query)
    for f in j["features"]:
        if not 'locality' in f['properties'].keys():
            logger.warning("No locality in answer '%s' for query='%s'" % (str(f['properties']),query))
            continue
        if len(j["features"]) == 1 or f['properties']['locality'].lower() == commune.lower():
            lon, lat = f["geometry"]["coordinates"]
            break
    
    if lat is None and not adresse is None:
        lon, lat = findCoordFromAddress(nom=nom, adresse=None,cp=cp,commune=commune,logger=logger)
        
    if lat is None and not nom is None:
        lon, lat = findCoordFromAddress(nom=None, adresse=None,cp=cp,commune=commune,logger=logger)
        
    if lat is None and not cp is None:
        lon, lat = findCoordFromAddress(nom=None, adresse=None,cp=None,commune=commune,logger=logger)

    if lat is None:
        logger.error("geoloc failed : %s, %s, %s, %s" % (nom,adresse,cp,commune))

    return lon, lat


if __name__ == '__main__':
    import doctest
    doctest.testmod()

