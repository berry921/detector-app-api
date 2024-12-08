# detector-app-api

物体検知API(detector-app-api)をAWS lambda上にコンテナデプロイするためのPythonコード一式。

下記pythonコードを実行して学習済みモデル model.pt を取得し、calculation.pyと同フォルダに予め配置しておくこと。

import torch\
import torchvision\
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)\
torch.save(model, "model.pt")

## AWS lambda上にコンテナデプロイする手順

1. AWS ECR (Elastic Container Registry)に適当なリポジトリを作成する。（ここではdetector-app-apiというリポジトリを作成したとする。）
2. 以下のdockerコマンドを実行し、コンテナイメージをビルド。\
$ docker build -t detector-app-api .
3. 以下のdockerコマンドを実行し、AWS ECRにプッシュできるようタグを付ける。\
$ docker tag detector-app-api \<your_aws_account_id\>.dkr.ecr.ap-northeast-1.amazonaws.com/detector-app-api:latest
4. 以下のaws configure ssoコマンドを実行し、ログインプロファイルを設定。\
$ <span style="color:green">**aws configure sso**</span>\
SSO session name (Recommended): <span style="color:red">***my-sso***</span>\
SSO start URL [None]: <span style="color:red">***\<your_aws_access_portal_url\>***</span>\
SSO region [None]: <span style="color:red">***ap-northeast-1***</span>\
SSO registration scopes [None]: <span style="color:red">***sso:account:access***</span>\
\
CLI default client Region [None]: <span style="color:red">***ap-northeast-1***</span>**\<ENTER\>**\
CLI default output format [None]: <span style="color:red">***json***</span>**\<ENTER\>**\
CLI profile name [123456789011_ReadOnly]: <span style="color:red">***my-dev-profile***</span>**\<ENTER\>**
5. 以下のawsコマンドを実行し、AWS ECRにdocker pushできるようログインする。\
$ aws ecr get-login-password --profile my-dev-profile | docker login --username AWS --password-stdin \<your_aws_account_id\>.dkr.ecr.ap-northeast-1.amazonaws.com
6. 以下のdockerコマンドを実行し、AWS ECRにコンテナイメージをプッシュ。\
$ docker push \<your_aws_account_id\>.dkr.ecr.ap-northeast-1.amazonaws.com/detector-app-api:latest
7. AWS LAMBDAで「関数を作成」を選択。上記手順でECRにプッシュしたコンテナイメージから関数を作成する。
8. 関数作成後、メモリを3008MBに設定し、関数URLを作成すれば完成。