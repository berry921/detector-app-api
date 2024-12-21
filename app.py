import os
from flask import Flask
from bp import api
from config import config
from a2wsgi import WSGIMiddleware
from mangum import Mangum

config_name = os.environ.get("CONFIG", "local")

app = Flask(__name__)
app.config.from_object(config[config_name])
# blueprintをアプリに登録
app.register_blueprint(api)

# FlaskアプリをASGIアプリに変換
asgi_app = WSGIMiddleware(app)
# Lambda用のMangumハンドラー
handler = Mangum(asgi_app)
