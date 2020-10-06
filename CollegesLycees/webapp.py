from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello_world():
    db = import_geoloc_db()
    k = list(db.values())[0]
    return str(k)


if __name__ == '__main__':
    app.run(debug=True)

