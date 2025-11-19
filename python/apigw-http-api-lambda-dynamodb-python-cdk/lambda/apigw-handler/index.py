# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import os
import json
import logging
import uuid
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Patch all supported libraries for X-Ray tracing
patch_all()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")


def handler(event, context):
    table = os.environ.get("TABLE_NAME")
    request_id = context.request_id
    
    # Log request details for audit
    logger.info(json.dumps({
        "event": "request_received",
        "request_id": request_id,
        "source_ip": event.get("requestContext", {}).get("identity", {}).get("sourceIp"),
        "user_agent": event.get("requestContext", {}).get("identity", {}).get("userAgent"),
        "http_method": event.get("requestContext", {}).get("http", {}).get("method"),
    }))
    
    try:
        if event["body"]:
            item = json.loads(event["body"])
            logger.info(f"Processing item: {json.dumps(item)}")
            year = str(item["year"])
            title = str(item["title"])
            id = str(item["id"])
            
            dynamodb_client.put_item(
                TableName=table,
                Item={"year": {"N": year}, "title": {"S": title}, "id": {"S": id}},
            )
            logger.info(f"Successfully inserted item with id: {id}")
            
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Successfully inserted data!"}),
            }
        else:
            logger.info("No payload provided, inserting default data")
            item_id = str(uuid.uuid4())
            dynamodb_client.put_item(
                TableName=table,
                Item={
                    "year": {"N": "2012"},
                    "title": {"S": "The Amazing Spider-Man 2"},
                    "id": {"S": item_id},
                },
            )
            logger.info(f"Successfully inserted default item with id: {item_id}")
            
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Successfully inserted data!"}),
            }
    except Exception as e:
        logger.error(json.dumps({
            "event": "error",
            "request_id": request_id,
            "error_type": type(e).__name__,
            "error_message": str(e),
        }))
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal server error"}),
        }
