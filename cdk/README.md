# Deploying Natal Chart Generation with AWS CDK

## Prerequisites

Create an AWS account and an Administrative User. See [here](https://cdkworkshop.com/15-prerequisites/200-account.html).

## Architecture

[Insert Diagram]

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
3. Install requirements
```
pip install -r requirements.txt
```
4. Install AWS CDK
```
npm install -g aws-cdk
``` 
5. Configure AWS credentials. This will require the ID and secret of your access key. See [here](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html).
```
aws configure
```
6. Deploy CDK stack
```
cdk deploy 
```

## Deployment via GitHub Actions

[TODO]
