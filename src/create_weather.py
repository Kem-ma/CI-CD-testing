import json, os, uuid
import boto3


def lambda_handler(event, context=None):
    try:
        data = json.loads(event.get("body") or "{}")
        item = {"id": str(uuid.uuid4()), **data}
        boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]).put_item(Item=item)
        return {"statusCode": 201, "body": json.dumps(item)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
