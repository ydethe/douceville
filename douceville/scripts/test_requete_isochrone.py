import os

from geoalchemy2.shape import to_shape
import geoalchemy2.functions as func

from douceville.blueprints.isochrone.geographique import calcIsochrone
from douceville.models import db, Etablissement, Resultat


os.environ[
    "OPENROUTESERVICE_KEY"
] = "5b3ce3597851110001cf6248b3fbd66e5be24021b1ea77cb39f76783"

iso = calcIsochrone([1.39396, 43.547864], 500)

pts = iso["features"][0]["geometry"]["coordinates"][0]

pg = "POLYGON(("
for lon, lat in pts:
    pg += "%f %f," % (lon, lat)
pg = pg[:-1] + "))"

a = Etablissement.query.filter(Etablissement.UAI == "0312290W").first()
print(a.asDict())

a = Etablissement.query.filter(
    func.ST_Within(Etablissement.position, func.ST_GeomFromEWKT(pg))
).filter(Etablissement.nature == "lycee")
print(a.count())

for r in a.all():
    print(r.nom)
