import sys
import urllib.parse
import urllib.request
import json


def send_image(url, image):
    # read image data
    with open(image, "rb") as f:
        reqbody = f.read()
    f.close()

    # create request with urllib
    req = urllib.request.Request(
        url=url,
        data=reqbody,
        method="POST",
        headers={"Content-Type": "application/octet-stream"}
    )
    with urllib.request.urlopen(req) as res:
        print(json.loads(res.read()))


if __name__ == "__main__":
    url, image = sys.argv[1], sys.argv[2]
    send_image(url, image)
