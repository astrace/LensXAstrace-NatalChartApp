import io
import os
import json
import uuid
from datetime import datetime

import boto3

from prototype import generate

import time

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    location_str = event["queryStringParameters"]["location_string"]
    datetime_str = event["queryStringParameters"]["datetime_string"]
    # datetime_str = '09/19/22 13:55:26'
    dt = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

    print('generating ...')
    t1 = time.perf_counter()
    im = generate(location_str, dt)
    t2 = time.perf_counter()
    print('Done. Time:', t2 - t1)

    # Save the image to an in-memory file
    tempfile = '/tmp/image.png'
    im.save(tempfile)
    
    key = "gen-images/" + "-".join([dt.strftime("%Y-%m-%d"), str(uuid.uuid4())[:8]])
    
    print('Uploading image to S3...')
    t1 = time.perf_counter()
    s3.upload_file(
        tempfile,
        os.environ['BUCKET_NAME'],
        key
    )
    t2 = time.perf_counter()
    print('Done. Time:', t2 - t1)
    print('Generating pre-signed url ...')
    t1 = time.perf_counter()
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': os.environ['BUCKET_NAME'],
            'Key': key
        },
        ExpiresIn=24 * 3600
    )
    t2 = time.perf_counter()
    print('Done. Time:', t2 - t1)
    responseObject = {
        "statusCode": 200,
        "headers": {"Contect-Type": "application/json"},
        "body": json.dumps({"preSignedUrl": url})
    }
    
    return responseObject

