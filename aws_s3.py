import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def upload_to_s3(file_name, bucket_name, object_name=None):
    """
    AWS S3にファイルをアップロードする関数

    :param file_name: ローカルファイルパス
    :param bucket_name: アップロード先のS3バケット名
    :param object_name: S3でのオブジェクト名 (デフォルトはローカルファイル名)
    """
    if object_name is None:
        object_name = file_name

    # S3クライアントを作成
    s3_client = boto3.client('s3')

    try:
        # ファイルをアップロード
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"{file_name} を {bucket_name}/{object_name} にアップロードしました。")
    except FileNotFoundError:
        print(f"エラー: {file_name} が見つかりませんでした。")
    except NoCredentialsError:
        print("エラー: AWS認証情報が見つかりませんでした。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


def download_from_s3(bucket_name, object_name, file_name=None):
    """
    AWS S3からファイルをダウンロードする関数

    :param bucket_name: S3バケット名
    :param object_name: S3上のオブジェクト名 (ダウンロード対象)
    :param file_name: ローカルファイルパス (デフォルトはオブジェクト名と同じ)
    """
    if file_name is None:
        file_name = object_name

    # S3クライアントを作成
    s3_client = boto3.client('s3')

    try:
        # S3からファイルをダウンロード
        s3_client.download_file(bucket_name, object_name, file_name)
        print(f"{bucket_name}/{object_name} を {file_name} にダウンロードしました。")
    except FileNotFoundError:
        print(f"エラー: ローカルパス {file_name} が無効です。")
    except NoCredentialsError:
        print("エラー: AWS認証情報が見つかりませんでした。")
    except PartialCredentialsError:
        print("エラー: AWS認証情報が不完全です。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
