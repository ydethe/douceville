import logging

from flask import jsonify, request
from flask_login import login_required
from geoalchemy2.shape import to_shape
from sqlalchemy import func, select
from sqlalchemy.orm import Session


from . import enseignement_bp


@enseignement_bp.route("/", methods=["GET"])
@login_required
def enseignement():
    from ...models import Etablissement, get_engine
    from ...utils import Serializer
    from ...blueprints.isochrone.geographique import calcIsochrone

    logger = logging.getLogger("douceville_logger")
    token = request.args.get("token", "")
    if token == "":
        return jsonify({})

    s = Serializer()
    dat = s.deserialize(token)
    logger.debug("enseignement param : %s" % str(dat))

    year = dat.get("year", 2018)
    lat = dat.get("lat", 1.39396)
    lon = dat.get("lon", 43.547864)
    dist = dat.get("dist", 600)
    transp = dat.get("transp", "")
    nature = dat.get("nature", [])
    secteur = dat.get("secteur", [])
    stat_min = dat.get("stat_min", 0)

    center = [lon, lat]
    iso = calcIsochrone(center, dist, transp)

    pts = iso["features"][0]["geometry"]["coordinates"][0]

    pg = "POLYGON(("
    for lon, lat in pts:
        pg += "%f %f," % (lon, lat)
    pg = pg[:-1] + "))"

    engine = get_engine()
    with Session(engine) as session:
        stmt = select(Etablissement).where(
            func.ST_Within(Etablissement.position, func.ST_GeomFromEWKT(pg))
        )

        if nature != []:
            stmt = stmt.where(Etablissement.nature.in_(nature))

        if secteur != []:
            stmt = stmt.where(Etablissement.secteur.in_(secteur))

        a = session.scalars(stmt)

        features = []
        for e in a.all():
            info = "<b>[%s]%s</b>" % (e.UAI, e.nom)

            stat = 0
            for res in e.resultats:
                if res.admis is not None and res.annee == int(year):
                    stat = int(100 * res.admis / res.presents)
                    info += "<br>Réussite %s %i : %i%%" % (res.diplome, res.annee, stat)

            if stat >= float(stat_min):
                p = to_shape(e.position)
                lon, lat = p.coords.xy
                f = {
                    "geometry": {"coordinates": [lon[0], lat[0]], "type": "Point"},
                    "properties": {"info": info},
                    "type": "Feature",
                }
                features.append(f)

    return jsonify(features)
