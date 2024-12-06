from fastapi.testclient import TestClient

from douceville.rest_api_entreypoint import app
from douceville.helpers import create_access_token
from douceville.schemas import DvUser, Isochrone


client = TestClient(app)


def test_me_with_auth():
    test_user = DvUser(
        id=2,
        login="test",
        admin=False,
        active=True,
    )
    token = create_access_token(data=test_user)
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.status_code
    usr = response.json()
    assert usr["login"] == "test"
    assert usr["id"] == 2


def test_me_without_auth():
    response = client.get("/me")
    assert response.status_code == 401, response.status_code


def test_isochrone():
    test_user = DvUser(
        id=2,
        login="test",
        admin=False,
        active=True,
    )
    token = create_access_token(data=test_user)
    params = dict(
        lat=45,
        lon=2,
        dist=600,
        transp="driving-car",
    )
    response = client.get("/isochrone", params=params, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.status_code
    iso = Isochrone(**response.json())
    assert iso.lonlat[0] == params["lon"]
    assert iso.lonlat[1] == params["lat"]
    assert iso.dist == params["dist"]
    assert iso.transp == params["transp"]
    assert len(iso.geometry) >= 3


if __name__ == "__main__":
    # test_me_without_auth()
    # test_me_with_auth()
    test_isochrone()
