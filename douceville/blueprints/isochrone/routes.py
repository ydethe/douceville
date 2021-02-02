from flask import jsonify, request
from flask_login import login_required, current_user

from douceville import logger
from douceville.utils import logged, Serializer
from douceville.blueprints.isochrone import isochrone_bp
from douceville.blueprints.isochrone.geographique import calcIsochrone


@isochrone_bp.route("/", methods=["GET"])
@login_required
def isochrone():
    token = request.args.get("token", "")
    if token == "":
        return jsonify({})

    s = Serializer()
    dat = s.deserialize(token)
    logger.debug("isochrone param : %s" % str(dat))

    dist = dat.get("dist", 600)
    transp = dat.get("transp", "")
    lat = dat.get("lat", 1.39396)
    lon = dat.get("lon", 43.547864)

    center = [lon, lat]
    iso = calcIsochrone(center, dist, transp)

    return jsonify(iso)
