# 😎 Object Detection API 😎

Codes for deploying an object detection API as a container image on AWS Lambda. By deploying this API to AWS Lambda, you can obtain object detection result like example below.\
This API uses the Mask R-CNN model with a ResNet-50-FPN backbone based on the [Mask R-CNN paper](https://arxiv.org/abs/1703.06870).

**Example Object Detection Result**\
<img src='./marlion.jpg' alt='before' width='800px'></img>
```shell
{'backpack0': 99, 'cell phone1': 99, 'person10': 91, 'person11': 91, 'person12': 90, 
'person2': 99, 'person3': 98, 'person4': 98, 'person5': 97, 'person6': 97, 'person7': 94, 
'person8': 92, 'person9': 92}
```
**（Reference Book）\
<font size="3">[Introduction to Web Application Development with Python Flask - How to Create an Object Detection App & Machine Learning API -](https://www.shoeisha.co.jp/book/detail/9784798175164)</font>**\
Written by Masaki Sato and Tetsuya Hirata, Supervised by Manabu Terada, Published by Shoeisya\
(Japanese Book)

## Preparation

1. Install Python, Git, Docker, and AWS CLI on your computing environment.\
Refer to respective tools' web pages for your installation.

2. Clone this repository, and change to the cloned folder by following commands:
```shell
$ git clone https://github.com/berry921/detector-app-api.git
$ cd detector-app-api
```
3. Create a Python virtual environment by venv.
```shell
$ python -m venv .venv    # virtual environment name (.venv) can be selected which you like.
```
4. Activate the virtual environment, and install torch and torchvision.
```shell
$ . .venv\bin\activate
$ pip install torch==1.13.1+cpu torchvision==0.14.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu
```
5. Download pre-trained model (model.pt) by following command:
```shell
$ python download_model.py
```
6. Create an AWS S3 bucket named 'detector-app-api-tmp'.\
(This bucket will be used by this API to store image files generated after object detection.)

## Deploying procedure to AWS Lambda

1. Create a repository at AWS ECR.\
(The following description assumes that you create a repository named 'detector-app-api'.)

2. Build container image by following Docker command:
```shell
$ docker build --platform linux/amd64 -t detector-app-api .
```
3. Tag the container image for pushing to AWS ECR:
```shell
$ docker tag detector-app-api <your_aws_account_id>.dkr.ecr.<your_aws_region>.amazonaws.com/detector-app-api:latest
```
4. Set up login profile for your AWS account by following AWS-CLI command:
```shell
$ aws configure sso
SSO session name (Recommended): my-sso
SSO start URL [None]: <your_aws_access_portal_url>
SSO region [None]: <your_aws_region>
SSO registration scopes [None]: sso:account:access

CLI default client Region [None]: <your_aws_region>
CLI default output format [None]: json
CLI profile name [123456789011_ReadOnly]: my-dev-profile # You can change the profile name as needed. Please adjust the --profile argument in the next step accordingly.
```
5. Log in to AWS ECR by following AWS CLI command:
```shell
$ aws ecr get-login-password --profile my-dev-profile | docker login --username AWS --password-stdin <your_aws_account_id>.dkr.ecr.<your_aws_region>.amazonaws.com
```
6. Push the container image to AWS ECR by following Docker command:
```shell
$ docker push <your_aws_account_id>.dkr.ecr.<your_aws_region>.amazonaws.com/detector-app-api:latest
```
7. Create a Lambda function from the container image pushed to AWS ECR.

8. In general settings of AWS Lambda, set memory size to 3008MB, and timeout to 3 minutes.

9. Create a function URL with authentication type set to None.

10. Grant the Lambda function access to the previously created AWS S3 bucket. Specifically, create a policy with the following JSON in AWS IAM and attach it to the Lambda function's IAM role:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowDetectorAppApiToAccessS3",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::detector-app-api-tmp/*"
            ]
        }
    ]
}
```

## How to Use After Deploying to AWS Lambda

1. Execute object detection API by following command to receive detection results:
```shell
python send_image.py <{your_aws_lambda_function_url}/detect> <path_to_your_image_file> --scale <scale>
# The scale argument is optional (if not specified, it defaults to 1080).
# Increasing the scale above 1080 improves detection accuracy by increasing the image size during detection, but it might cause an error if it exceeds Lambda's memory size limit (3008MB).
# Therefore, increase the scale is not recommended.
# Even with the default value (1080), an error might occur. In such cases, please reduce the scale as needed.
```
2. Download the image file with detection results by following command:
```shell
python download_image.py <{your_aws_lambda_function_url}/download> <path_to_download_image_file>
```