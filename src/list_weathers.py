import json, os
import boto3


def lambda_handler(event, context=None):
    try:
        res = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]).scan()
        return {"statusCode": 200, "body": json.dumps(res.get("Items", []), default=str)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
