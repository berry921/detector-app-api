import os

from a2wsgi import WSGIMiddleware
from flask import Flask
from mangum import Mangum

from blueprint import api
from config import config

config_name = os.environ.get("CONFIG", "local")

app = Flask(__name__)
app.config.from_object(config[config_name])
app.register_blueprint(api)

# transform Flask app to ASGI app
asgi_app = WSGIMiddleware(app)
# Mangum handler for Lambda
handler = Mangum(asgi_app)
