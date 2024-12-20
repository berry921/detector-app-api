import sys
import urllib.parse
import urllib.request


def download_image(url, result_file_path):
    with urllib.request.urlopen(url) as web_file:
        with open(result_file_path, "wb") as local_file:
            local_file.write(web_file.read())


if __name__ == "__main__":
    url, result_file_path = sys.argv[1], sys.argv[2]
    download_image(url, result_file_path)
