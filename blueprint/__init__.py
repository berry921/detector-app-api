from flask import Blueprint, request, jsonify, make_response
import calculation
from aws_s3 import download_from_s3

api = Blueprint("api", __name__)


@api.get("/")
def index():
    return jsonify({"column": "value"}), 201


@api.post("/detect")
def detection():
    # requestからパラメータ scale を取得
    scale = request.form.get("scale", type=int)
    if scale is None:
        return jsonify({'error': "Missing 'scale' parameter"}), 400

    # requestから画像を取得
    image = request.files.get('image')
    if image is None:
        return jsonify({'error': "Missing 'image' file"}), 400

    return calculation.detection(image, scale)


@api.get("/download")
def download():
    response = make_response()
    download_from_s3('detector-app-api-tmp', 'tmp.jpg', '/tmp/tmp.jpg')
    response.data = open('/tmp/tmp.jpg', "rb").read()
    response.headers['Content-Disposition'] = 'attachment; filename=result.jpg'
    response.mimetype = "image/jpeg"
    return response
