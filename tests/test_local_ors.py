import requests


def test_ors():
    # query='   mon école dans les collines, Pouylebon, Gers, France'
    query = "Pouylebon, Gers, France"
    url = "https://photon.komoot.io/api/?q={query}"
    res = requests.get(url.format(query=query))
    print(res.json())


if __name__ == "__main__":
    test_ors()
