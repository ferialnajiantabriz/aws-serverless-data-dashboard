import os
import boto3
import pandas as pd
import streamlit as st
from boto3.dynamodb.conditions import Attr


REGION = os.getenv('AWS_REGION', 'us-east-1')
TABLE = os.getenv('TABLE_NAME', 'serverless-dashboard-dev-events')


st.title("AWS Serverless Data Dashboard (Local Demo)")


session = boto3.Session(region_name=REGION)
ddb = session.resource('dynamodb')
table = ddb.Table(TABLE)


st.write("Querying last 24h events from DynamoDB…")
resp = table.scan()
items = resp.get('Items', [])


df = pd.DataFrame(items)
if not df.empty:
st.metric("Events (total)", len(df))
st.bar_chart(df['event_type'].value_counts())
st.dataframe(df)
else:
st.info("No data yet. Send a POST to /event first.")