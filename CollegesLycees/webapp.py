from flask import Flask

from conv_rdf import import_geoloc_db


app = Flask(__name__)

@app.route('/')
def hello_world():
    db = import_geoloc_db()
    k = list(db.values())[0]
    return str(k)

