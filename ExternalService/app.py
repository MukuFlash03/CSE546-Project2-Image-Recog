#!/usr/bin/env python3

import boto3

session = boto3.Session()
sqs = session.client('sqs')
lambda_client = session.client('lambda')
s3 = session.client('s3')

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
                lambda_client.invoke(
                    FunctionName=lambda_function_name,
                    InvocationType='Event',
                    Payload=body
                )
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
    except Exception as exp:
        print("Some error occured while monitoring SQS: ",exp)

