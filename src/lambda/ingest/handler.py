import os, json, time, uuid
import boto3


ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['TABLE_NAME'])


def lambda_handler(event, context):
body = event.get('body') if isinstance(event, dict) else None
if body and isinstance(body, str):
try:
payload = json.loads(body)
except json.JSONDecodeError:
return {"statusCode": 400, "body": json.dumps({"error": "Invalid JSON"})}
elif isinstance(event, dict):
payload = event.get('payload', {})
else:
payload = {}


item = {
'pk': str(uuid.uuid4()),
'ts': int(time.time()),
'source': payload.get('source', 'unknown'),
'event_type': payload.get('event_type', 'click'),
'meta': payload.get('meta', {}),
}


table.put_item(Item=item)


return {
"statusCode": 200,
"headers": {"Content-Type": "application/json"},
"body": json.dumps({"ok": True, "item": item})
}