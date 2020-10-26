import os

from openrouteservice import client


def calcIsochrone(center, dist):
    # https://openrouteservice.org/dev/#/home?tab=1
    api_key = os.environ["OPENROUTESERVICE_KEY"]
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
