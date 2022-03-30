import json
import os
from datetime import datetime

import boto3

DYNAMO_TABLE = os.environ.get("DYNAMO_TABLE")
dynamo = boto3.client('dynamodb')


def handler(event, context):
    # TODO: Figure out why FilterExpression is not working...
    # date = datetime.now().strftime('%Y-%m-%d')
    # filter_exp = f"begins_with(timestamp, '{date}')"

    response = dynamo.scan(TableName=DYNAMO_TABLE)
    method = event['httpMethod']
    if method == "GET":
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response['Items'], indent=2)
        }
    else:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps("We only accept GET /")
        }
