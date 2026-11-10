import json, os
import boto3


def lambda_handler(event, context=None):
    try:
        item_id = event["pathParameters"]["id"]
        data = json.loads(event.get("body") or "{}")
        item = {**data, "id": item_id}
        boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]).put_item(Item=item)
        return {"statusCode": 200, "body": json.dumps(item)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
