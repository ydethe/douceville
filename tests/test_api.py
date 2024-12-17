import unittest

from fastapi.testclient import TestClient

from douceville import config
from douceville.server import app
from douceville.auth import create_access_token
from douceville.schemas import Etablissement, Isochrone, QueryParameters


class TestDoucevilleAPI(unittest.TestCase):
    def setUp(self):
        super().setUp()

        token = create_access_token(
            config.SUPABASE_URL,
            config.SUPABASE_KEY,
            config.SUPABASE_TEST_USER,
            config.SUPABASE_TEST_PASSWORD,
        )
        self.client = TestClient(app, headers={"Authorization": f"Bearer {token}"})

    def test_me_with_auth(self):
        response = self.client.get("/user")
        assert response.status_code == 200, response.status_code
        usr = response.json()

        assert usr["login"] == config.SUPABASE_TEST_USER

    def test_openapi(self):
        response = self.client.get("/openapi.json")
        assert response.status_code == 200, response.status_code

    def test_isochrone(self):
        params = dict(
            lat=43.6085909,
            lon=1.4401531,
            dist=600,
            transp="driving-car",
        )
        response = self.client.get("/isochrone", params=params)
        assert response.status_code == 200, response.status_code
        iso = Isochrone(**response.json())
        assert iso.lonlat[0] == params["lon"]
        assert iso.lonlat[1] == params["lat"]
        assert iso.dist == params["dist"]
        assert iso.transp == params["transp"]
        assert len(iso.geometry) >= 3

    def test_etablissement(self):
        response = self.client.get("/etablissement/X42Y")
        assert response.status_code == 200, response.status_code
        data = response.json()
        data.pop("resultats", [])
        etab = Etablissement(**data)
        assert etab.UAI == "X42Y"

    def test_etablissements_zone(self):
        params = dict(
            lat=43.6085909,
            lon=1.4401531,
            dist=600,
            transp="driving-car",
        )
        response = self.client.get("/isochrone", params=params)
        assert response.status_code == 200, response.status_code
        iso = Isochrone(**response.json())

        body = QueryParameters(year=2020, stat_min=0, iso=iso)
        response = self.client.post("/etablissements", json=body.model_dump())
        assert response.status_code == 200, response.status_code
        data = response.json()
        assert len(data) > 0


if __name__ == "__main__":
    a = TestDoucevilleAPI()

    a.setUp()
    a.test_openapi()

    # a.setUp()
    # a.test_me_with_auth()

    # a.setUp()
    # a.test_isochrone()

    # a.setUp()
    # a.test_etablissement()

    # a.setUp()
    # a.test_etablissements_zone()
