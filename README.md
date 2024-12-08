# 物体検知API

物体検知APIをAWS lambda上にコンテナデプロイするためのコード一式です。

下記pythonコードを実行して学習済みモデル model.pt を取得し、calculation.pyと同フォルダに予め配置してください。

import torch\
import torchvision\
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)\
torch.save(model, "model.pt")

## AWS lambda上にコンテナデプロイする手順

1. AWS ECR (Elastic Container Registry)にリポジトリを作成。* 以下はdetector-app-apiという名称のリポジトリを作成したとする。
2. 下記dockerコマンドを実行し、コンテナイメージをビルド。\
$ docker build -t detector-app-api .
3. 下記dockerコマンドを実行し、AWS ECRにプッシュできるようタグ付け。\
$ docker tag detector-app-api *\<your_aws_account_id\>*.dkr.ecr.*\<your_aws_region\>*.amazonaws.com/detector-app-api:latest
4. 下記aws configure ssoコマンドを実行し、ログインプロファイルを設定。
\
$ ***aws configure sso***\
SSO session name (Recommended): ***my-sso***\
SSO start URL [None]: ***\<your_aws_access_portal_url\>***\
SSO region [None]: ***\<your_aws_region\>***\
SSO registration scopes [None]: ***sso:account:access***\
\
CLI default client Region [None]: ***\<your_aws_region\>***\
CLI default output format [None]: ***json***\
CLI profile name [123456789011_ReadOnly]: ***my-dev-profile***

5. 下記awsコマンドを実行し、AWS ECRにログイン。\
$ aws ecr get-login-password --profile *my-dev-profile* | docker login --username *AWS* --password-stdin *\<your_aws_account_id\>*.dkr.ecr.*\<your_aws_region\>*.amazonaws.com
6. 下記dockerコマンドを実行し、コンテナイメージをAWS ECRへプッシュ。\
$ docker push *\<your_aws_account_id\>*.dkr.ecr.*\<your_aws_region\>*.amazonaws.com/detector-app-api:latest
7. AWS LAMBDAで、AWS ECRへプッシュしたコンテナイメージから関数を作成。
8. 関数作成後、メモリを3008MBに設定し、関数URLを作成すれば完成。