# AWS API Gateway HTTP API to AWS Lambda in VPC to DynamoDB CDK Python Sample!

## Overview

Creates an [AWS Lambda](https://aws.amazon.com/lambda/) function writing to [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) and invoked by [Amazon API Gateway](https://aws.amazon.com/api-gateway/) REST API with comprehensive throttling controls following AWS Well-Architected Framework REL05-BP02.

![architecture](docs/architecture.png)

## Throttling Configuration (REL05-BP02 Compliance)

This implementation includes multiple layers of request throttling to prevent resource exhaustion:

### API Gateway Throttling
- **Rate Limit**: 100 requests/second
- **Burst Limit**: 200 requests
- Returns `429 Too Many Requests` when exceeded

### Usage Plans & API Keys
- **Per-client Rate Limit**: 50 requests/second
- **Per-client Burst Limit**: 100 requests
- Requires API key for access

### Lambda Reserved Concurrency
- **Reserved Executions**: 50 concurrent executions
- Prevents account-level concurrency exhaustion

### AWS WAF Rate Limiting
- **IP-based Limit**: 2000 requests per 5 minutes per IP
- Automatic blocking of malicious traffic
- CloudWatch metrics enabled

## Setup

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Deploy
At this point you can deploy the stack. 

Using the default profile

```
$ cdk deploy
```

With specific profile

```
$ cdk deploy --profile test
```

## After Deploy

### Get API Key
After deployment, retrieve the API key from AWS Console or CLI:
```bash
aws apigateway get-api-keys --include-values
```

### Test the API
Navigate to AWS API Gateway console and test the API with the API key header:

**Headers:**
```
x-api-key: YOUR_API_KEY_HERE
Content-Type: application/json
```

**Sample Request Body:**
```json
{
    "year":"2023", 
    "title":"kkkg",
    "id":"12"
}
```

**Expected Response:**
```json
{"message": "Successfully inserted data!"}
```

### Throttling Test
To test throttling, send requests exceeding the configured limits:
- Without API key: Should get 403 Forbidden
- Exceeding rate limits: Should get 429 Too Many Requests

## Cleanup 
Run below script to delete AWS resources created by this sample stack.
```
cdk destroy
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!