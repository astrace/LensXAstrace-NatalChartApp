from io import BytesIO
import json
import os
import tempfile
import uuid
import boto3
from natal_chart import generate

def handler(event, context):
    local_time = event['queryStringParameters']['local_time']
    location = event['queryStringParameters']['location']

    im = generate(local_time, location)
    
    # Save image to temporary file
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file_path = os.path.join(tmp_dir, 'natal_chart.png')
        im.save(tmp_file_path, format='PNG')
        
        # Upload file to S3 bucket
        s3 = boto3.resource('s3')
        bucket_name = os.environ['NATAL_CHART_BUCKET_NAME']
        print("NATAL_CHART_BUCKET_NAME", os.environ['NATAL_CHART_BUCKET_NAME'])
        bucket = s3.Bucket(bucket_name)
        
        filename = f"{local_time.split('T')[0]}_{str(uuid.uuid4())[:8]}.png"
        
        image_buffer = BytesIO()
        im.save(image_buffer, format='PNG')
        image_buffer.seek(0)
        
        bucket.upload_fileobj(
            image_buffer, filename,
            ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
        )
        
    # Return URL of uploaded image
    image_url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'image/png'},
        'body': json.dumps({'url': image_url})
    }

