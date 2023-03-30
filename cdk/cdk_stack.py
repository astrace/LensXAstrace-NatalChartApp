from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
)

import os
import tempfile

class NatalChartCdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 Bucket to store image layers
        img_layer_bucket = s3.Bucket(self, "ImageLayerBucket")

        # Deploy the image layers to the bucket
        img_layer_deployment = s3deploy.BucketDeployment(
            self,
            "ImageLayerDeployment",
            sources=[s3deploy.Source.asset("../app/assets/images")],
            destination_bucket=img_layer_bucket,
            memory_limit=1024
        )

        # Lambda Layer for Python dependencies
        # Create a temporary directory to install dependencies
        with tempfile.TemporaryDirectory() as tmpdir:
            # Install dependencies to temporary directory
            os.system(f"pip install -r ../app/requirements.txt --target {tmpdir}")

            # Define Lambda layer for dependencies
            dep_layer = _lambda.LayerVersion(
                self, "NatalChartDependenciesLayer",
                code=_lambda.Code.from_asset(tmpdir), 
                compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
            )

        # TODO: copy all files into temp dir + lambda dir

        # Lambda Layer for main Python program
        # Create a temporary directory to install & zip
        with tempfile.TemporaryDirectory() as tmpdir:
            filenames = [
                "../app/natal_chart_cli.py",
                "../app/natal_chart.py",
                "../app/utils.py",
                "../app/image_params.py",
                "../app/constants.py",
            ]
            os.system(f"zip {tmpdir}/app.zip {' '.join(filenames)}")

            # Define Lambda layer for dependencies
            app_layer = _lambda.LayerVersion(
                self, "AppLayer",
                code=_lambda.Code.from_asset(f"{tmpdir}/app.zip"), 
                compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
            )

        # Lambda Function
        lambda_fn = _lambda.Function(
            self, "NatalChartLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="natal_chart.handler",
            code=_lambda.Code.from_asset(path="lambda"),
            layers=[dep_layer, app_layer],
            environment={
                "IMG_LAYER_BUCKET_NAME": img_layer_bucket.bucket_name
            }
        )

        # API Gateway
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=lambda_fn
        )

        # TODO: Restrict API access to only our frontend

