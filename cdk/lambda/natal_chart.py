import json
import subprocess

def handler(event, context):
    birth_date = event['queryStringParameters']['birth_date']
    location = event['queryStringParameters']['location']

    result = subprocess.run(
        ['python', 'natal_chart_cli.py', birth_date, location],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode != 0:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': result.stderr})
        }

    image_url = None # TODO
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'image/png'},
        'body': image_url
    }

