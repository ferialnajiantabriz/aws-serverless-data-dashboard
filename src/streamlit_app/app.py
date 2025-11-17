import os
import boto3
import pandas as pd
import streamlit as st

REGION = os.getenv("AWS_REGION", "us-east-1")
TABLE = os.getenv("TABLE_NAME", "serverless-dashboard-dev-events")

st.title("AWS Serverless Data Dashboard (Local Demo)")

# Create DynamoDB client
session = boto3.Session(region_name=REGION)
ddb = session.resource("dynamodb")
table = ddb.Table(TABLE)

st.write("Querying events from DynamoDB…")

resp = table.scan()
items = resp.get("Items", [])

df = pd.DataFrame(items)

if not df.empty:
    # All lines in this block are indented with 4 spaces
    st.metric("Events (total)", len(df))

    # If event_type exists, show a bar chart of counts
    if "event_type" in df.columns:
        counts = df["event_type"].value_counts()
        st.bar_chart(counts)

    st.dataframe(df)
else:
    st.info("No data yet. Send a POST to /event first.")
