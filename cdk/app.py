#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_stack import NatalChartCdkStack

app = cdk.App()
NatalChartCdkStack(app, "natal-chart-cdk")

app.synth()

