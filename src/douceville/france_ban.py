from dataclasses import dataclass

import requests
import urllib.parse


@dataclass
class ResultatBAN:
    longitude: float
    latitude: float
    score: float
    housenumber: str
    name: str
    postcode: str
    city: str
    district: str
    street: str


def requete_ban(query: str) -> ResultatBAN:
    from .config import config

    dat = requests.get(f"http://{config.ADDOK_HOST}:7878/search?q={urllib.parse.quote(query)}")
    data = dat.json()

    dat = data["features"][0]

    res = ResultatBAN(
        longitude=dat["geometry"]["coordinates"][0],
        latitude=dat["geometry"]["coordinates"][1],
        score=dat["properties"].get("score", None),
        housenumber=dat["properties"].get("housenumber", None),
        name=dat["properties"].get("name", None),
        postcode=dat["properties"].get("postcode", None),
        city=dat["properties"].get("city", None),
        district=dat["properties"].get("district", None),
        street=dat["properties"].get("street", None),
    )

    return res
