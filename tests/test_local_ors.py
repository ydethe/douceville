from openrouteservice import Client


def test_ors():
    coords = ((8.34234, 48.23424), (8.34423, 48.26424))

    # key can be omitted for local host
    client = Client(base_url="http://localhost:8082/ors")

    # Only works if you didn't change the ORS endpoints manually
    routes = client.directions(coords)

    # If you did change the ORS endpoints for some reason
    # you'll have to pass url and required parameters explicitly:
    routes = client.request(
        url="/new_url",
        post_json={"coordinates": coords, "profile": "driving-car", "format": "geojson"},
    )

    print(routes)


if __name__ == "__main__":
    test_ors()
