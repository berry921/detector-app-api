from pathlib import Path
from flask import Flask, request, make_response
from aws_s3 import download_from_s3
from a2wsgi import WSGIMiddleware
from mangum import Mangum
from config import config
import calculation


basedir = Path(__name__).parent


app = Flask(__name__)
app.config.from_object(config["base"])


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        json_results, _ = calculation.detection(request)
        return json_results, _
    elif request.method == "GET":
        response = make_response()
        download_from_s3('pytorch-model-bucket-inaharu', 'tmp.jpg', '/tmp/tmp.jpg')
        response.data = open('/tmp/tmp.jpg', "rb").read()
        downloadFileName = "result.jpg"
        response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName
        response.mimetype = "image/jpeg"
        return response


# FlaskアプリをASGIアプリに変換
asgi_app = WSGIMiddleware(app)
# Lambda用のMangumハンドラー
handler = Mangum(asgi_app)
