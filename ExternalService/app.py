import json

import boto3

session = boto3.Session()
sqs = session.client('sqs')
lambda_client = session.client('lambda')
s3 = boto3.resource('s3')
bucket_name = 'output-bucket-results231'
queue_name = "p3-sqs-1"
queue_url = "https://sqs.us-east-1.amazonaws.com/874290406143/p3-sqs-1"
lambda_function_name = "fae_recognition"

while True:
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            WaitTimeSeconds=10,
            VisibilityTimeout=2
        )
        if 'Messages' in response:
            for message in response['Messages']:
                body = message['Body']
                records = json.loads(body)
                for record in records['Records']:
                    if record['s3']['bucket']['name'] == 'input-bucket-1523':
                        lambda_client.invoke(
                            FunctionName=lambda_function_name,
                            InvocationType='Event',
                            Payload=body
                        )
                    else:
                        object_key = record['s3']['object']['key']
                        bucket = s3.Bucket(bucket_name)
                        result_object = bucket.Object(object_key)
                        result = result_object.get()['Body'].read().decode('utf-8')
                        print("Output for {} is {}".format(object_key,result))
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
    except Exception as exp:
        print("Some error occured while monitoring SQS: ",exp)


