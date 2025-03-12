# Job Sheet: AWS Lambda with CloudWatch Logging and SNS Notification

Set up an AWS Lambda function (`my-app`) with CloudWatch logging and SNS notifications for error detection.

### Steps Covered:
1. Creating an AWS Lambda function.
2. Assigning necessary IAM policies.
3. Enabling CloudWatch logging.
4. Configuring CloudWatch metric filters for error detection.
5. Setting up SNS notifications for alerts.
6. Deploying and testing AWS Lambda scripts.
7. Verifying error monitoring and alerts.

## **Step 1: Create AWS Lambda Function**

1. Go to **AWS Lambda** → **Create Function**.
2. Select **Author from scratch**.
3. Enter the function name: `my-app`.
4. Runtime: Choose `Python 3.x`.
5. Select an **IAM role**:

   - Choose **Create a new role with basic Lambda permissions**.
6. Click **Create function**.
7. **Important:** Before proceeding, manually trigger the Lambda function once to ensure that the CloudWatch log group (`/aws/lambda/my-app`) is created automatically.|

   - If the log group does not appear, re-run the function and refresh the CloudWatch log groups page.

## **Step 2: Attach IAM Policies**

Lambda needs permissions to access CloudWatch Logs and SNS.

1. Go to **IAM** → **Roles**.
2. Find and select the role created for `my-app`.
3. Click **Add permissions** → **Attach policies**.
4. Attach the following policies:
   - `AWSLambdaBasicExecutionRole`

   - `CloudWatchFullAccess`

   - `SNSFullAccess`

   - **Custom inline policy** (Name: `LambdaCloudWatchSNSPolicy`):
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": [
             "logs:CreateLogGroup",
             "logs:CreateLogStream",
             "logs:PutLogEvents",
             "logs:FilterLogEvents"
           ],
           "Resource": "arn:aws:logs:us-east-1:440744255146:log-group:/aws/lambda/my-app:*"
         },
         {
           "Effect": "Allow",
           "Action": "sns:Publish",
           "Resource": "arn:aws:sns:us-east-1:440744255146:CloudWatchAlertsTopic"
         }
       ]
     }
     ```
5. Click **Save changes**.

## **Step 3: Enable CloudWatch Logging**

1. Go to **AWS Lambda** → Select **`my-app`**.
2. Click **Configuration** → **Monitoring and operations tools**.
3. Ensure that **Amazon CloudWatch Logs** is enabled.

## **Step 4: Verify CloudWatch Logs Exist**

1. Go to **AWS CloudWatch** → **Logs** → **Log groups**.
2. Find `/aws/lambda/my-app`.
3. Click on it and check for log streams when the function runs.

   - If no logs appear, manually invoke the function again.

## **Step 5: Create CloudWatch Metric Filter**

1. Go to **AWS CloudWatch** → **Logs** → **Log groups** → `/aws/lambda/my-app`.
2. Click the **Metric filters** tab.
3. Click **Create metric filter**.
4. In **Filter pattern**, enter:

   ```

   ERROR

   ```
5. Click **Next** and set:
   - **Metric namespace**: `LambdaMonitoring`
   - **Metric name**: `LambdaErrorCount`
   - **Metric value**: `1`
6. Click **Create filter**.

## **Step 6: Create CloudWatch Alarm for SNS Notifications**

1. Go to **AWS CloudWatch** → **Logs** → **Log groups** → `/aws/lambda/my-app`.
2. Click the **Metric filters** tab.
3. Select the **Lambda Error Filter** checkbox.
4. Click **Create alarm**.
5. Set:
   - **Threshold type**: Static
   - **Whenever LambdaErrorCount is ≥ 1 for 1 period (5 minutes)**
6. Click **Next** and choose:
   - **Notification type**: **Send a notification to an SNS topic**
   - **SNS Topic**: `CloudWatchAlertsTopic`
7. Click **Create alarm**.

## **Step 7: Deploy and Test the Setup**

1. Manually trigger **`my-app`** Lambda function.
2. Check **CloudWatch Logs** under `/aws/lambda/my-app`.
3. Ensure **errors** are detected in logs.
4. Confirm **CloudWatch Alarm** triggers an **SNS notification**.

## **Step 8: Implement AWS Lambda Python Scripts**

### **Important Notes:**

- **Run the first script (****`Script Test Error`****) first to verify logs appear in CloudWatch.**
- **Once confirmed, use the second script (****`Script for Automatic Error Detection`****) to enable automatic monitoring and SNS alerts.**

### **Script Test Error (Manually Trigger an Error)**

```python
import boto3
import logging

# Logging Configuration
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Initialize SNS Client
sns_client = boto3.client('sns')

# Replace with the ARN of your existing SNS topic
sns_topic_arn = "arn:aws:sns:us-east-1:123456789012:YourExistingSNSTopic"

def lambda_handler(event, context):
    try:
        # Simulate Error
        raise ValueError("This is a forced error to trigger CloudWatch Alarm!")
    except Exception as e:
        logger.error(f"Lambda Function Error: {str(e)}")
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="🚨 Lambda Function Error Alert!",
            Message=f"An error occurred in Lambda: {str(e)}"
        )
    return {
        'statusCode': 500,
        'body': "Error has been triggered and notified!"
    }
```

### **Script for Automatic Error Detection**

```python
import json
import boto3
import os

def get_cloudwatch_logs(log_group_name, filter_pattern):
    client = boto3.client('logs')
    response = client.filter_log_events(
        logGroupName=log_group_name,
        filterPattern=filter_pattern,
        limit=5
    )
    return response['events']

def send_sns_notification(message):
    sns_client = boto3.client('sns')
    sns_topic_arn = os.environ['SNS_TOPIC_ARN'] # Replace with the ARN of your existing SNS topic
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='CloudWatch Log Alert'
    )

def lambda_handler(event, context):
    LOG_GROUP = '/aws/lambda/my-app'
    FILTER_PATTERN = 'ERROR'
    logs = get_cloudwatch_logs(LOG_GROUP, FILTER_PATTERN)
    if logs:
        log_messages = '\n'.join([log['message'] for log in logs])
        send_sns_notification(f'Error Logs Detected:\n{log_messages}')
    return {
        'statusCode': 200,
        'body': json.dumps('Execution completed!')
    }
```

## **Step 9: Verify and Monitor AWS Lambda Error Alerts**

1. Navigate to **AWS CloudWatch** → **Logs** → **Log groups** → `/aws/lambda/my-app` → **Check if error logs appear**.
2. Go to **CloudWatch Alarms** → **Select ****`LambdaErrorCount`**** alarm**.
3. Ensure the alarm status changes when an error is detected.
4. Verify that SNS notifications are received in your email.
5. Regularly monitor logs and alarms to ensure proper functionality.
