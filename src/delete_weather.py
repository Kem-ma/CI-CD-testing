import json, os
import boto3


def lambda_handler(event, context=None):
    try:
        item_id = event["pathParameters"]["id"]
        boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]).delete_item(Key={"id": item_id})
        return {"statusCode": 200, "body": json.dumps({"deleted": item_id})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
