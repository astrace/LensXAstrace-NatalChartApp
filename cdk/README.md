# Deploying Natal Chart Generation with AWS CDK

This directory contains the AWS CDK code for deploying the Natal Chart generation program to various AWS
services. The services included in this deployment are AWS Lambda, Amazon S3, Amazon API Gateway, and Amazon
CloudFront.

![High-level Architecture Diagram](./assets/aws_architecture.png)

## Architecture Overview

1. AWS Lambda: A Python function that processes natal chart generation requests and stores the generated images in an Amazon S3 bucket.
2. Amazon S3: Two buckets are used for storing image layers and generated natal charts.
3. Amazon API Gateway: Provides a RESTful API for the Lambda function, allowing clients to submit natal chart requests. The API Gateway is restriced to the domain of the frontend.
4. Amazon CloudFront: A CDN that efficiently serves the image layers stored in the Amazon S3 bucket.

## Prerequisites

Create an AWS account and an Administrative User. See [here](https://cdkworkshop.com/15-prerequisites/200-account.html).

## Continuous Deployment via GitHub Actions

AWS CDK app is deployed whenever there are changes made to this directory on the `production` branch. See [this](../.github/workflows/deploy-cdk-stack.yml) GitHub actions workflow.

## Local Deployment

**Note**: We require Python 3.7 for our development environment because we make use of
the experimental AWS CDK [Python Library](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda_python_alpha/README.html)
which is only available for Python 3.7:

https://pypi.org/project/aws-cdk.aws-lambda-python-alpha/


This library makes it a lot easier to deploy Python Lambda functions.

---

1. [Install](https://docs.docker.com/engine/install/) and run Docker.
2. Install [Python 3.7](https://www.python.org/downloads/release/python-370/).
3. Set up a Python 3.7 virtual environment.
```
pip3.7 install virtualenv
python3.7 -m virtualenv <venv_name>
source <venv_name>/bin/activate
```
4. Install requirements
```
pip install -r requirements.txt
```
5. Install AWS CDK
```
npm install -g aws-cdk
``` 
6. Configure AWS credentials. This will require the ID and secret of your access key. See [here](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html).
```
aws configure
```
7. Ensure that the `FRONTEND_DOMAIN_NAME` environment variable is correctly set.
8. Deploy CDK stack
```
cdk deploy 
```

## Amazon API Gateway URL

The Amazon API Gateway provides a RESTful API for the Lambda function.
You can find the URL of the API Gateway in the CDK output:
```
ApiGatewayUrl: https://xxxxxx.execute-api.region.amazonaws.com/prod

```
