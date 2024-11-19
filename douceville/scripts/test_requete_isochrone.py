import geoalchemy2.functions as func

from douceville.blueprints.isochrone.geographique import calcIsochrone
from douceville.models import Etablissement


iso = calcIsochrone([1.39396, 43.547864], 500, "driving-car")

pts = iso["features"][0]["geometry"]["coordinates"][0]

pg = "POLYGON(("
for lon, lat in pts:
    pg += "%f %f," % (lon, lat)
pg = pg[:-1] + "))"

a = Etablissement.query.filter(Etablissement.UAI == "0312290W").first()
print(a.asDict())

a = Etablissement.query.filter(func.ST_Within(Etablissement.position, func.ST_GeomFromEWKT(pg)))
print(a.count())

for r in a.all():
    print(r.nom)
