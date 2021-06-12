import simplejson as json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'CountVisitors'
table = dynamodb.Table(table_name)
ID = '0'


# import requests


def lambda_handler(event, context):
    response = table.get_item(
        Key={
            'ID': ID
        }
    )

    if 'Item' in response:
        response = table.update_item(
            Key={
                'ID': ID
            },
            UpdateExpression="set visitorcount = visitorcount + :N",
            ExpressionAttributeValues={
                ':N': 1
            }
        )
        response = table.get_item(
            Key={
                'ID': ID
            }
        )
        visitsresponse = {
            "statusCode": 200,
            'headers': {
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET'
            },
            "body": json.dumps({
                        "counter": response['Item'].get('visitorcount'),
            }),
        }
        visits = json.loads(visitsresponse["body"])
        return visits["counter"]
    else:
        print("There was an error")

