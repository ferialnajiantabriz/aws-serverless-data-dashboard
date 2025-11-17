#!/usr/bin/env bash
set -euo pipefail
STACK_NAME=serverless-dashboard-dev
REGION=${1:-us-east-1}


aws cloudformation deploy \
--template-file template.yaml \
--stack-name $STACK_NAME \
--capabilities CAPABILITY_NAMED_IAM \
--region $REGION


aws cloudformation describe-stacks \
--stack-name $STACK_NAME \
--region $REGION \
--query 'Stacks[0].Outputs'