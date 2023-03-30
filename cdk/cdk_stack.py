from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda_python_alpha as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
)
from aws_cdk.aws_lambda import Runtime

import os
import tempfile

class NatalChartCdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ### SET UP S3 BUCKETS

        # image layers
        img_layer_bucket = s3.Bucket(self, "ImageLayerBucket")
        # ephemerides
        ephe_bucket = s3.Bucket(self, "EphemeridesBucket")

        # Deploy buckets
        s3deploy.BucketDeployment(
            self,
            "ImageLayerDeployment",
            sources=[s3deploy.Source.asset("../app/assets/images")],
            destination_bucket=img_layer_bucket,
            memory_limit=1024
        )
        s3deploy.BucketDeployment(
            self,
            "EphemeridesDeployment",
            sources=[s3deploy.Source.asset("../app/assets/ephe/")],
            destination_bucket=ephe_bucket,
            memory_limit=1024
        )

        # copy main program files into lambda folder
        filenames = [
            "../app/natal_chart.py",
            "../app/utils.py",
            "../app/image_params.py",
            "../app/constants.py",
        ]
        os.system(f"cp {' '.join(filenames)} lambda")

        # Lambda Function
        lambda_fn = _lambda.PythonFunction(
            self, "NatalChartLambdaFunction",
            entry="lambda",
            runtime=Runtime.PYTHON_3_7,
            index="lambda.py",
            handler="handler",
            layers=[
                _lambda.PythonLayerVersion(
                    self, "DependenciesLayer", entry="../app"
                )
            ],
            environment={
                "IMG_LAYER_BUCKET_NAME": img_layer_bucket.bucket_name,
                "EPHE_BUCKET_NAME": ephe_bucket.bucket_name
            },
            timeout=Duration.seconds(60)
        )

        img_layer_bucket.grant_read(lambda_fn)
        ephe_bucket.grant_read(lambda_fn)
        # TODO: grant write to generate images directory

        # API Gateway
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=lambda_fn
        )

        # TODO: Restrict API access to only our frontend

