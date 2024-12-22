import requests
import argparse


def send_image(url, image, scale):
    # read image data
    with open(image, "rb") as f:
        file = {'image': f.read()}
    f.close()

    data = {"scale": scale}

    with requests.post(url, data=data, files=file) as response:
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="upload image to AWS lambda function url and detect.")
    parser.add_argument('url', type=str, help="your AWS lambda function url. Don't forget to add '/detect' to the end of your URL")
    parser.add_argument('image', type=str, help="image file path to detect. jpeg format.")
    parser.add_argument('--scale', type=int, default=1080, help="image scale (default: 1080)")
    args = parser.parse_args()
    send_image(args.url, args.image, args.scale)
