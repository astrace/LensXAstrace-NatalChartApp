import json
import subprocess
from natal_chart import generate


def handler(event, context):
    local_time = event['queryStringParameters']['local_time']
    location = event['queryStringParameters']['location']

    im = generate(local_time, location)
    
    # TODO: check for error
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'image/png'}, # TODO: return correct file
        'body': image_url
    }

