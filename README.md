# **AWS Serverless Data Dashboard (Event Ingestion + Daily Analytics Pipeline)**

A fully implemented, production-style **serverless analytics pipeline** built on AWS.
This project ingests real-time events, stores them in DynamoDB, aggregates daily metrics using scheduled Lambdas, and visualizes results through a Streamlit dashboard.

The system demonstrates practical cloud engineering ability, event-driven architecture, and hands-on deployment of multiple AWS services working together seamlessly.

---

## ** High-Level Overview**

This pipeline follows a widely used pattern in real-world systems such as:

* product analytics
* marketing funnel tracking
* IoT device events
* user behavior monitoring
* app telemetry pipelines

**Flow:**

1. Clients send events (click, signup, view, etc.)
2. API Gateway receives and validates the request
3. Lambda stores the event in DynamoDB
4. EventBridge triggers a nightly aggregation
5. Another Lambda builds a daily summary
6. Summary JSON goes into S3
7. Streamlit dashboard reads DynamoDB for analytics

---

## **🏗️ Architecture**

![Architecture](docs/architecture.png)

---

## **✨ Key Features**

### ** Real-Time Event Ingestion API**

A public HTTP endpoint handles event ingestion through API Gateway → Lambda → DynamoDB.

Example request:

```json
POST /event
{
  "source": "web",
  "event_type": "click",
  "meta": { "user": "demo" }
}
```

The ingestion Lambda automatically:

* generates a unique primary key (`pk`)
* assigns a timestamp (`ts`)
* stores the event in DynamoDB
* returns the saved record

---

### ** Automated Daily Aggregation**

Every night at midnight UTC, EventBridge triggers an aggregation Lambda that:

* scans DynamoDB for the last 24 hours
* groups events by type
* calculates counts
* generates a summary document
* uploads it to S3 in folder:

```
daily_summaries/YYYY-MM-DD.json
```

Example output from S3:

![Summary](docs/s3_summary_sample.png)

---

### ** Interactive Local Analytics Dashboard (Streamlit)**

A lightweight UI for exploring the ingested data:

* total event count
* bar chart of event types
* raw event table
* auto-refreshes when new data arrives

Run locally:

```bash
source .venv/bin/activate
export AWS_REGION=us-east-1
export TABLE_NAME=serverless-dashboard-dev-events
cd src/streamlit_app
streamlit run app.py
```

Dashboard example:

![Dashboard](docs/dashboard_sample.png)

---

## ** Tech Stack**

### **AWS Services**

* **Lambda (Python)** — compute for ingestion & aggregation
* **DynamoDB** — high-performance NoSQL event store
* **API Gateway (HTTP API)** — public ingestion endpoint
* **EventBridge** — nightly cron scheduler
* **S3** — archive of daily rollups
* **CloudWatch** — logging & alarms
* **CloudFormation** — infrastructure-as-code

### **Local Tools**

* Streamlit (dashboard)
* Python 3.12
* boto3 (AWS SDK)
* requests

---

## ** Deployment**

Deploy the full stack (Lambdas, API Gateway, DynamoDB, EventBridge, S3, IAM roles):

```bash
./scripts/deploy.sh us-east-1
```

Remove everything:

```bash
./scripts/teardown.sh us-east-1
```

Validate the CloudFormation template manually:

```bash
aws cloudformation validate-template \
  --template-body file://template.yaml \
  --region us-east-1
```

---

## ** Repository Structure**

```
aws-serverless-data-dashboard/
│
├── src/
│   ├── ingest/           # Lambda: event ingestion
│   ├── aggregate/        # Lambda: daily aggregation
│   └── streamlit_app/    # Local dashboard
│
├── scripts/
│   ├── deploy.sh         # Automated stack deployment
│   └── teardown.sh       # Automated resource cleanup
│
├── docs/
│   ├── architecture.png
│   ├── dashboard_sample.png
│   ├── dynamodb_sample.png
│   └── s3_summary_sample.png
│
├── template.yaml         # Full CloudFormation stack
└── README.md
