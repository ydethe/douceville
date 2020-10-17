import os

from sqlalchemy import not_, or_

from flask import render_template
from geojson import Feature, Point, FeatureCollection
import geojson

from CollegesLycees.config import basedir
from CollegesLycees import app
from CollegesLycees.models import Etablissement


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Yann'}
    return render_template('index.html', title='Home', user=user)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/map')
def map():
    a = Etablissement.query.filter(Etablissement.departement==31).filter(not_(Etablissement.latitude.is_(None))).all()

    l_feat = []
    for e in a:
        if e.admis_brevet is None or e.presents_brevet is None:
            continue
        if e.admis_brevet/e.presents_brevet < 0.98:
            continue
        # if e.admis_gt is None or e.presents_gt is None:
        #     continue
        # if e.admis_gt/e.presents_gt < 0.98:
        #     continue
        print(e.UAI, e.nom, e.commune)
        f = {"geometry": {"coordinates": [e.longitude, e.latitude], "type": "Point"}, "properties": {"nom": e.nom}, "type": "Feature"}
        l_feat.append(f)
    feat_coll = FeatureCollection(l_feat)
    js = geojson.dumps(feat_coll)
    with open(os.path.join(basedir,'static','toto.geojson'), 'w') as f:
        f.write(js)
    return render_template('map.html', geojson_file='static/toto.geojson')

