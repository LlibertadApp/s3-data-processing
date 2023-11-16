
import boto3
import os
import json
import psycopg2

# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

def handler(event, context):

  aws_region = os.getenv('AWS_REGION')
  # db_xxxx = os.getenv('DB_XXXX')
  # stage = input['STAGE']
  missingInputsList = []

  if ('aws_region' not in locals()) or (aws_region == ""):
    missingInputsList.append("AWS_REGION")
  # if ('db_xxxx' not in locals()) or (db_xxxx == ""):
  #   missingInputsList.append("DB_XXXX")
  # if ('stage' not in locals()) or (stage == ""):
  #   missingInputsList.append("STAGE")
  if (missingInputsList):
    raise MissingParameters("Missing required input: " + ", ".join(missingInputsList) )

  s3 = boto3.resource('s3', region_name=aws_region)
  sqs = boto3.client('sqs', region_name=aws_region)



  # print('environment variables:\n', os.environ.keys())
  for event_record in event['Records']:
    event_payload_text = event_record["body"]
    # print(str(event_payload_text))
    event_payload = json.loads(event_payload_text)
    records = event_payload.get('Records', [])  # Obtener la lista de registros
    for s3_record in records:
      bucket_arn  = s3_record['s3']['bucket']['arn']
      bucket_name = s3_record['s3']['bucket']['name']
      object_key  = s3_record['s3']['object']['key']
      print(f"bucket_arn: {bucket_arn}\n")
      print(f"bucket_name: {bucket_name}\n")
      print(f"object_key: {object_key}\n")

      s3_object = s3.Object(bucket_name, object_key)
      s3_object_data = s3_object.get()['Body'].read().decode('utf-8') 

      print(s3_object_data)


