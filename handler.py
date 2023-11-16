import json
import logging
import os

import boto3
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

QUEUE_URL = os.getenv('QUEUE_URL')
BUCKET_NAME = os.getenv('BUCKET_NAME')
SQS = boto3.client('sqs')
S3 = boto3.resource('s3')


def consumer(event, context):
    for record in event['Records']:
        logger.info(f'Message body: {record["body"]}')
        s3payload = json.loads(record['Body'])

        content_object = s3.Object(BUCKET_NAME, s3payload['baseKey']);
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)

        logger.info(
            json_content
        )
