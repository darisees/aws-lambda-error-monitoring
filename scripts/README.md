# Scripts for AWS Lambda Error Monitoring

This directory contains Python scripts used for AWS Lambda error monitoring and notification.

## Available Scripts

### 1. `test_error.py`
This script is designed to manually trigger an error in an AWS Lambda function. It helps verify that errors are correctly logged in CloudWatch and that SNS notifications are sent properly.

#### How It Works:
- Simulates an intentional error (`ValueError`) in the Lambda function.
- Logs the error to CloudWatch.
- Sends an SNS notification about the error.

#### When to Use:
- To test if CloudWatch Logs capture errors correctly.
- To verify that SNS notifications are properly configured and delivered.

### 2. `error_monitor.py`
This script automatically monitors CloudWatch Logs for errors and sends an SNS notification when an error is detected.

#### How It Works:
- Retrieves logs from CloudWatch based on a predefined log group.
- Filters log events to identify error messages.
- Sends an SNS notification with error details if any are found.

#### When to Use:
- For real-time monitoring of AWS Lambda failures.
- To automate error detection and alerting.

## Setup Instructions
1. Deploy the scripts in AWS Lambda.
2. Ensure the Lambda function has the necessary IAM permissions to access CloudWatch and SNS.
3. Configure environment variables as needed (e.g., SNS Topic ARN).
4. Test using `test_error.py` before deploying `error_monitor.py` for automated monitoring.

## Notes
- The `test_error.py` script should be run first to confirm that logging and SNS are set up correctly.
- Once verified, deploy `error_monitor.py` for continuous error monitoring.
- Ensure the correct IAM role permissions are assigned to Lambda.

## Contribution
Feel free to contribute by improving the playbooks, adding new automation features, or optimizing configurations.
