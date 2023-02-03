import requests
from io import BytesIO

import boto3
from PIL import Image

import constants

def load_image(filename):
    url = constants.IMAGES_URL + filename
    print("Loading {} ...".format(url))
    resp = requests.get(url)
    im = Image.open(BytesIO(resp.content))
    return im

def read_image_from_s3(bucket, key, region_name='us-east-1'):
    """Load image file from s3.

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    np array
        Image array
    """
    print('Reading {} from S3 bucket {} ...'.format(key, bucket))
    s3 = boto3.client('s3')
    file_byte_string = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    x = BytesIO(file_byte_string)
    return Image.open(BytesIO(file_byte_string))
    
def write_image_to_s3(im, bucket, key, region_name='us-east-1'):
    """Write an image array into S3 bucket

    Parameters
    ----------
    im: PIL.Image.Image
        Image
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    None
    """
    s3 = boto3.resource('s3', region_name)
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    file_stream = BytesIO()
    im.save(file_stream, format='png')
    object.put(Body=file_stream.getvalue())
