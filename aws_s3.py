import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def upload_to_s3(file_name, bucket_name, object_name=None):
    """
    Function to upload a file to AWS S3

    :param file_name: Local file path
    :param bucket_name: S3 bucket name
    :param object_name: Object name in S3 (default: same as local file name)
    """
    if object_name is None:
        object_name = file_name

    # Create S3 client
    s3_client = boto3.client("s3")

    try:
        # Upload a file
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"Uploaded {file_name} to {bucket_name}/{object_name}.")
    except FileNotFoundError:
        print(f"Error: Not found {file_name}.")
    except NoCredentialsError:
        print("Error: AWS Credential is not found.")
    except Exception as e:
        print(f"Error: {e}")


def download_from_s3(bucket_name, object_name, file_name=None):
    """
    Function to download a file from AWS S3.

    :param bucket_name: S3 bucket name
    :param object_name: Object name in S3 (Object to download)
    :param file_name: Local file path (default: same as object name)
    """
    if file_name is None:
        file_name = object_name

    # Create S3 client
    s3_client = boto3.client("s3")

    try:
        # downdload a file from S3
        s3_client.download_file(bucket_name, object_name, file_name)
        print(f"Downloaded {file_name} from {bucket_name}/{object_name}.")
    except FileNotFoundError:
        print(f"Error: Not found {bucket_name}/{object_name}.")
    except NoCredentialsError:
        print("Error: AWS Credential is not found.")
    except PartialCredentialsError:
        print("Error: AWS Credential is imcomplete.")
    except Exception as e:
        print(f"Error {e}")
