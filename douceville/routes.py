from flask import render_template
from sqlalchemy import distinct

from douceville import app
from douceville.models import db, Etablissement


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Yann"}
    r = db.session.query(distinct(Etablissement.nature)).all()

    return render_template(
        "index.html", title="Home", user=user, natures=[x[0] for x in r]
    )
