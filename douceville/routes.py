from sqlalchemy import not_, distinct
from geoalchemy2.shape import to_shape
from geoalchemy2 import func

from flask import render_template, jsonify, make_response, request

from douceville.config import Config
from douceville import app
from douceville.models import db, Etablissement, Resultat
from douceville.isochrone import calcIsochrone, findCoordFromAddress
from douceville.utils import logged, Serializer


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Yann"}
    r = db.session.query(distinct(Etablissement.nature)).all()

    return render_template(
        "index.html", title="Home", user=user, natures=[x[0] for x in r]
    )


@app.route("/points", methods=["GET"])
def get_all_points():
    token = request.args.get("token", "")
    
    s = Serializer()
    dat = s.deserialize(token)
    # dat = {'nature':nature, 'departement':departement, 'dist':dist, 'lon':lon, 'lat':lat}
    year = dat.pop('year', 2018)
    nature = dat.pop('nature', '0')
    departement = dat.pop('departement', 0)
    stat_min = dat.pop('stat_min', 0)
    dist = dat.pop('dist', 600)
    lat = dat.pop('lat', 1.39396)
    lon = dat.pop('lon', 43.547864)
    
    center = [lon, lat]
    iso = calcIsochrone(center, dist)

    pts = iso["features"][0]["geometry"]["coordinates"][0]

    pg = "POLYGON(("
    for lon, lat in pts:
        pg += "%f %f," % (lon, lat)
    pg = pg[:-1] + "))"

    a = Etablissement.query.filter(not_(Etablissement.position.is_(None))).filter(
        func.ST_Within(Etablissement.position, func.ST_GeomFromEWKT(pg))
    )

    if departement > 0:
        a = a.filter(Etablissement.departement == departement)

    if nature != "0":
        a = a.filter(Etablissement.nature == nature)

    features = []
    for e in a.all():
        info = "<b>[%s]%s</b>" % (e.UAI, e.nom)

        results = (
            Resultat.query.filter(Resultat.etablissement_id == e.UAI)
            .filter(Resultat.annee == year)
            .all()
        )

        stat = 0
        for res in results:
            if not res.admis is None:
                stat = int(100 * res.admis / res.presents)
                info += "<br>Réussite %s : %i%%" % (res.diplome, stat)

        if stat >= stat_min:
            p = to_shape(e.position)
            lon, lat = p.coords.xy
            f = {
                "geometry": {"coordinates": [lon[0], lat[0]], "type": "Point"},
                "properties": {"info": info},
                "type": "Feature",
            }
            features.append(f)

    return jsonify(features)

@app.route("/isochrone", methods=["GET"])
def isochrone():
    token = request.args.get("token", "")

    s = Serializer()
    dat = s.deserialize(token)
    # dat = {'nature':nature, 'departement':departement, 'dist':dist, 'lon':lon, 'lat':lat}
    year = dat.pop('year', 2018)
    nature = dat.pop('nature', '0')
    departement = dat.pop('departement', 0)
    stat_min = dat.pop('stat_min', 0)
    dist = dat.pop('dist', 600)
    lat = dat.pop('lat', 1.39396)
    lon = dat.pop('lon', 43.547864)
    
    center = [lon, lat]
    iso = calcIsochrone(center, dist)
    
    return jsonify(iso)

@app.route("/map", methods=["GET"])
def map():
    year = int(request.args.get("year", "2018"))
    nature = request.args.get("nature", "0")
    departement = int(request.args.get("departement", "0"))
    stat_min = int(request.args.get("stat_min", "0"))
    dist = float(request.args.get("dist", "300"))
    lon = float(request.args.get("lon", "1.39396"))
    lat = float(request.args.get("lat", "43.547864"))
    address = request.args.get("address", "")

    if address != '':
        lon,lat = findCoordFromAddress(address)

    s = Serializer()
    dat = {'year':year, 'nature':nature, 'departement':departement, 'dist':dist, 'lon':lon, 'lat':lat, 'stat_min':stat_min}
    token = s.serialize(dat)

    return render_template(
        "map.html",
        points_request="%s:%i/points?token=%s" % (Config.HOST, Config.PORT, token),
        isochrone_request="%s:%i/isochrone?token=%s" % (Config.HOST, Config.PORT, token),
    )
