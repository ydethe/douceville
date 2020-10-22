from gevent.pywsgi import WSGIServer

from maillage import app
from maillage.config import Config


# http_server = WSGIServer((Config.HOST, Config.PORT), app, keyfile='key.pem', certfile='cert.pem')
http_server = WSGIServer((Config.HOST, Config.PORT), app)
http_server.serve_forever()
