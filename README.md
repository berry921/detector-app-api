# 物体検知API

物体検知APIをAWS lambda上にコンテナデプロイするためのコード一式。

## 準備

1. 使用している環境にpython, git, dockerをインストール。
2. 下記コマンドを実行し、本リポジトリをclone。
```shell
$ git clone git@github.com:berry921/detector-app-api
```
3. 下記pythonコードを実行して学習済み物体検知モデル model.pt を取得し、calculation.pyと同フォルダに配置。
```python
import torch
import torchvision
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
torch.save(model, "model.pt")
```
## AWS lambdaへのコンテナデプロイ
1. AWS ECR (Elastic Container Registry)にリポジトリを作成。\
（以降の説明では、detector-app-apiという名称のリポジトリを作成したとする。）
2. 下記dockerコマンドを実行し、コンテナイメージをビルド。
```shell
$ docker build -t detector-app-api .
```
3. 下記dockerコマンドを実行し、AWS ECRにプッシュできるようタグ付け。
```shell
$ docker tag detector-app-api <your_aws_account_id>.dkr.ecr.<your_aws_region>.amazonaws.com/detector-app-api:latest
```
4. 下記aws configure ssoコマンドを実行し、ログインプロファイルを設定。
```shell
$ aws configure sso
SSO session name (Recommended): my-sso
SSO start URL [None]: <your_aws_access_portal_url>
SSO region [None]: <your_aws_region>
SSO registration scopes [None]: sso:account:access

CLI default client Region [None]: your_aws_region>
CLI default output format [None]: json
CLI profile name [123456789011_ReadOnly]: my-dev-profile
```
5. 下記awsコマンドを実行し、AWS ECRにログイン。
```shell
$ aws ecr get-login-password --profile my-dev-profile | docker login --username AWS --password-stdin <your_aws_account_id>.dkr.ecr.<your_aws_region>.amazonaws.com
```
6. 下記dockerコマンドを実行し、コンテナイメージをAWS ECRへプッシュ。
```shell
$ docker push <your_aws_account_id>.dkr.ecr.<your_aws_region>.amazonaws.com/detector-app-api:latest
```
7. AWS LAMBDAで、AWS ECRへプッシュしたコンテナイメージから関数を作成。
8. 関数作成後、メモリを3008MBに設定し、関数URLを作成。

## AWS lambdaへコンテナデプロイした後の使用方法

1. 下記のpythonコードを"send_image.py"といった名前を付けて保存。
```python:send_image.py
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
```
2. 下記コマンドを実行すると物体検知APIが実行され、検知結果が返ってくる。
```shell
$ python send_image.py <your_aws_lambda_function_url> <path_to_your_image_file>
```
3. 下記のpythonコードを"download_image.py"といった名前を付けて保存。
```python:download_image.py
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
```
4. 下記コマンドを実行すると物体検知APIで検知した結果を反映した画像ファイルをダウンロードできる。
```shell
$ python download_image.py <your_aws_lambda_function_url> <path_to_download_image_file>
```