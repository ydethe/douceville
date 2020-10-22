from gevent.pywsgi import WSGIServer

from maillage import app
from maillage.config import Config


http_server = WSGIServer(
    ("0.0.0.0", Config.PORT),
    app,
    keyfile="/home/user-data/ssl/ssl_private_key.pem",
    certfile="/home/user-data/ssl/ssl_certificate.pem",
)
# http_server = WSGIServer((Config.HOST, Config.PORT), app)
http_server.serve_forever()
