import os, json, time
import boto3
from datetime import datetime


ddb = boto3.resource('dynamodb')
s3 = boto3.client('s3')


def lambda_handler(event, context):
table_name = os.environ['TABLE_NAME']
bucket = os.environ['BUCKET_NAME']
table = ddb.Table(table_name)


now = int(time.time())
day_ago = now - 24*3600


resp = table.scan()
items = resp.get('Items', [])
items = [it for it in items if it.get('ts', 0) >= day_ago]


count = len(items)
by_type = {}
for it in items:
et = it.get('event_type', 'unknown')
by_type[et] = by_type.get(et, 0) + 1


summary = {
'timestamp': datetime.utcnow().isoformat()+"Z",
'count_24h': count,
'by_event_type': by_type,
}


key = f"daily_summaries/{datetime.utcnow().strftime('%Y-%m-%d')}.json"
s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(summary).encode('utf-8'))


return {'ok': True, 's3_key': key, 'summary': summary}