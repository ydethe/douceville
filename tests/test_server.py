from waitress import serve

from douceville.app import app


serve(app, listen="*:9978")
