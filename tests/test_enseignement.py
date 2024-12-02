# from base64 import b64encode


def test_enseignement(client):
    from douceville.utils import Serializer

    req_param = {}
    req_param["address"] = "24 rue de l'Hers, Saint Orens de Gameville"
    req_param["transp"] = ""
    req_param["dist"] = 60 * 30
    req_param["stat_min"] = 0
    req_param["nature"] = []
    req_param["secteur"] = []
    req_param["year"] = "2020"

    s = Serializer()
    token = s.serialize(req_param)

    response = client.get("/enseignement", follow_redirects=True, query_string={"token": token})
    print(response.json)


if __name__ == "__main__":
    from douceville.app import app

    with app.test_client() as client:
        test_enseignement(client)
