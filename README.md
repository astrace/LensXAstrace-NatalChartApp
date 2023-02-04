# Astrace Natal Chart Generation

TODO: High-level description

## Prerequisites

### AWS IAM

Make sure that `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in GitHub Actions Secrets maps to an AWS IAM User that has *at least* the permissions/policies defined in `template.yaml` and `.github/workflows/package-python-deps-aws-layer.yml`. That is, we need permissions to:
- deploy/update a Lambda layer
- deploy a Lambda function with the following permissions:
  - write access for logs
  - read access for S3 bucket containing planet images
  - read/write access for S3 bucket for storing generated natal chart images
  
The exact Amazon Resources are defined in the respective files.
  
TODO: Define the exact Amazon Resource Names in some top-level environment file.

TODO: Make sure following best practices: https://jayendrapatil.com/aws-iam-best-practices/

## Local Testing of Generation Algorithm

TODO

## Testing API Gateway

TODO

## Deployment

TODO
