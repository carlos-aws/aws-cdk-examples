
# AWS API Gateway HTTP API to AWS Lambda in VPC to DynamoDB CDK Python Sample!


## Overview

Creates an [AWS Lambda](https://aws.amazon.com/lambda/) function writing to [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) and invoked by [Amazon API Gateway](https://aws.amazon.com/api-gateway/) REST API. 

![architecture](docs/architecture.png)

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

### Retrieve API Key
After deployment, retrieve the API key value from AWS Systems Manager Parameter Store or API Gateway console:

```bash
aws apigateway get-api-keys --include-values --query "items[?name=='DemoApiKey'].value" --output text
```

### Test the API
Navigate to AWS API Gateway console or use curl to test the API. You must include the `x-api-key` header with your requests:

```bash
curl -X POST https://YOUR_API_ID.execute-api.REGION.amazonaws.com/prod/ \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"year":"2023", "title":"kkkg", "id":"12"}'
```

You should get below response:

```json
{"message": "Successfully inserted data!"}
```

### Usage Plan Limits
The API is protected with the following limits per API key:
- Rate limit: 10 requests per second
- Burst limit: 20 concurrent requests
- Daily quota: 10,000 requests

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
