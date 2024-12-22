import argparse
import urllib.parse
import urllib.request


def download_image(url, result_file_path):
    with urllib.request.urlopen(url) as web_file:
        with open(result_file_path, "wb") as local_file:
            local_file.write(web_file.read())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='download most recent detected image file.')
    parser.add_argument('url', type=str, help="your AWS lambda function url. Don't forget to add '/download' to the end of your URL.")
    parser.add_argument('image', type=str, help="image file path to be downloaded. jpeg format.")
    args = parser.parse_args()
    download_image(args.url, args.image)
