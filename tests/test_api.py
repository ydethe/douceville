import unittest

from fastapi.testclient import TestClient

from douceville.rest_api_entreypoint import app
from douceville.helpers import create_access_token
from douceville.schemas import DvUser, Etablissement, Isochrone


class TestDoucevilleAPI(unittest.TestCase):
    def setUp(self):
        super().setUp()

        test_user = DvUser(
            id=2,
            login="test",
            admin=False,
            active=True,
        )
        token = create_access_token(data=test_user)
        self.client = TestClient(app, headers={"Authorization": f"Bearer {token}"})

    def test_me_with_auth(self):
        response = self.client.get("/me")
        assert response.status_code == 200, response.status_code
        usr = response.json()
        assert usr["login"] == "test"
        assert usr["id"] == 2

    def test_isochrone(self):
        params = dict(
            lat=45,
            lon=2,
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
        response = self.client.get("/etablissement/0180766K")
        assert response.status_code == 200, response.status_code
        data = response.json()
        data.pop("resultats", [])
        etab = Etablissement(**data)
        assert etab.UAI == "0180766K"


if __name__ == "__main__":
    a = TestDoucevilleAPI()

    a.setUp()
    a.test_me_with_auth()

    a.setUp()
    a.test_isochrone()

    a.setUp()
    a.test_etablissement()
