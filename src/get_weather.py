import json, os
import boto3


def lambda_handler(event, context=None):
    try:
        item_id = event["pathParameters"]["id"]
        res = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]).get_item(Key={"id": item_id})
        if "Item" not in res:
            return {"statusCode": 404, "body": json.dumps({"error": "Not found"})}
        return {"statusCode": 200, "body": json.dumps(res["Item"], default=str)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
