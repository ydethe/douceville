import eventlet
from eventlet import wsgi

from douceville import logger
from douceville.app import app


wsgi.server(sock=eventlet.listen(("0.0.0.0", 3566)), site=app, log=logger, debug=False)
