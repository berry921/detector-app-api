# ベースイメージ
FROM public.ecr.aws/lambda/python:3.9.2024.11.22.15

# ディレクトリとファイルのコピー
COPY . ${LAMBDA_TASK_ROOT}

# pipのバージョン更新およびライブラリインストール
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Linux用PyTorchインストール
RUN pip install torch==1.13.1+cpu torchvision==0.14.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu

# "building..."を表示させる処理
RUN echo "building..."

# 特定のネットワークポートをコンテナ実行時にリッスン
EXPOSE 8080

# "docker run"実行時に実行される処理
CMD [ "app.handler" ]