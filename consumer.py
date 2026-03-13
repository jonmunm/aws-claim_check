import logging
import boto3
import pandas as pd
import csv
import json
from io import BytesIO

logger = logging.getLogger('consumer')
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
cloudwatch_client = boto3.client('cloudwatch')

def handler(event, context):

    record = event['Records'][0]
    sqs_body = json.loads(record['body'])
    bucket_name = sqs_body['detail']['bucket']['name']
    object_key = sqs_body['detail']['object']['key']
    
    logger.info(f"Processing file: s3://{bucket_name}/{object_key}")

    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response['Body'].read()
    file_size_mb = round(len(file_content) / 1024 / 1024, 2)

    df = pd.read_csv(
        BytesIO(file_content), 
        sep=None, 
        engine='python', 
        usecols=[0], 
        quoting=csv.QUOTE_NONE,
        encoding='utf-8',
        on_bad_lines='skip'
    )

    logger.info(f'Rows received: {df.shape[0]}')

    cloudwatch_client.put_metric_data(
        MetricData=[
            {
                'MetricName': 'ROWS',
                'Dimensions': [{'Name': 'Type', 'Value': 'Consumed'}],
                'Unit': 'Count',
                'Value': df.shape[0]
            },
        ],
        Namespace='Claim Check'
    )

    # 6. Enviar métrica: SIZE
    cloudwatch_client.put_metric_data(
        MetricData=[
            {
                'MetricName': 'SIZE',
                'Dimensions': [{'Name': 'Type', 'Value': 'Consumed'}],
                'Unit': 'Megabytes',
                'Value': file_size_mb
            },
        ],
        Namespace='Claim Check'
    )

    logger.info(f'Metrics sent: {df.shape[0]} rows, {file_size_mb} MB')