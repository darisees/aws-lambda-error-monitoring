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
