from flask import render_template

from douceville import app


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Yann"}

    return render_template("index.html", title="Home", user=user)
