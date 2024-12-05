from douceville.blueprints.isochrone.geographique import calcIsochrone


def test_calcul_isochrones():
    dist = 600
    transp = "driving-car"
    center = [1.515583, 43.569771]

    iso = calcIsochrone(center, dist, transp)

    return iso


def test_isochrones(client):
    from douceville.utils import Serializer

    req_param = {}
    req_param["address"] = "24 rue de l'Hers, Saint Orens de Gameville"
    req_param["transp"] = "driving-car"
    req_param["dist"] = 60 * 30
    req_param["stat_min"] = 0
    req_param["nature"] = []
    req_param["secteur"] = []
    req_param["year"] = "2020"

    s = Serializer()
    token = s.serialize(req_param)

    response = client.get(
        "/isochrone", follow_redirects=True, query_string={"token": token}
    )

    return response.json


if __name__ == "__main__":
    from douceville.app import app

    with app.test_client() as client:
        test_isochrones(client)

    # test_calcul_isochrones()
