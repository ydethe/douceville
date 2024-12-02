from flask import jsonify, request
from flask_login import login_required

from . import isochrone_bp
from .geographique import calcIsochrone


@isochrone_bp.route("/", methods=["GET"])
@login_required
def isochrone():
    from ... import logger
    from ...utils import Serializer

    token = request.args.get("token", "")
    if token == "":
        return jsonify({})

    s = Serializer()
    dat = s.deserialize(token)
    logger.debug("isochrone param : %s" % str(dat))

    dist = dat.get("dist", 600)
    transp = dat.get("transp", "driving-car")
    lat = dat.get("lat", 1.39396)
    lon = dat.get("lon", 43.547864)

    center = [lon, lat]
    iso = calcIsochrone(center, dist, transp)

    return jsonify(iso)
