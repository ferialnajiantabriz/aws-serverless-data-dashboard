#!/usr/bin/env bash
set -euo pipefail
STACK_NAME=serverless-dashboard-dev
REGION=${1:-us-east-1}


# Empty the S3 bucket before deletion
BUCKET=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION \
--query "Stacks[0].Outputs[?OutputKey=='BackupBucketName'].OutputValue" --output text)


if [ -n "$BUCKET" ]; then
aws s3 rm s3://$BUCKET --recursive || true
fi


aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION
aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME --region $REGION