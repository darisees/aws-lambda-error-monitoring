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
