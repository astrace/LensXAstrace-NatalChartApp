import io
import os
import json
import uuid
from datetime import datetime

import boto3

from prototype import generate
def lambda_handler(event, context):
    """Generates an astrological chart image and uploads it to S3, returning a pre-signed URL to access it.

        Args:
            event (dict): A dictionary containing parameters for generating the chart image, including:
                - location_string (str): A string representing the location of birth for the person the chart is for.
                - datetime_string (str): A string representing the date and time of birth for the person the chart is for, in the format 'MM/DD/YY HH:MM:SS'.
            context: Currently unused in this function. Placeholder for now.

        Returns:
            responseObject (dict): A dictionary containing 200 status response fields 
            + data payload (image), to send to server.
    """
    s3 = boto3.client('s3')

    location_str = event["queryStringParameters"]["location_string"]
    datetime_str = event["queryStringParameters"]["datetime_string"]

    # datetime_str = '09/19/22 13:55:26'
    dt = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

    im = generate(location_str, dt)

    # Save the image to an in-memory file
    tempfile = '/tmp/image.png'
    im.save(tempfile)
    
    key = "gen-images/" + "-".join([dt.strftime("%Y-%m-%d"), str(uuid.uuid4())[:8]])
    
    print('Uploading image to S3...')
    s3.upload_file(
        tempfile,
        os.environ['BUCKET_NAME'],
        key
    )
    print('Done.')
    print('Generating pre-signed url ...')
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': os.environ['BUCKET_NAME'],
            'Key': key
        },
        ExpiresIn=24 * 3600
    )
    print('Done.')
    responseObject = {
        "statusCode": 200,
        "headers": {"Contect-Type": "application/json"},
        "body": json.dumps({"preSignedUrl": url})
    }
    return responseObject

