# AWS Lambda Error Monitoring

Welcome to the **AWS Lambda Error Monitoring Repository**! This repository provides an automated solution for monitoring AWS Lambda errors using Amazon CloudWatch and SNS notifications. 

## 📂 Folder Structure

The repository contains the following directories and files:

- **`job-sheet/`** : Contains job sheets that explain the automation process in detail.
- **`scripts/`** : Stores Python scripts for testing and monitoring Lambda errors.
- **`.gitignore`** : Specifies which files should be ignored in version control.
- **`LICENSE`** : The license file for this repository.
- **`README.md`** : This document, providing an overview of the repository.

## 🌐 Features

- CloudWatch Log Monitoring  
- Automatic Error Detection  
- SNS Email Notifications  
- CloudWatch Alarms Integration  

## ⚡ Prerequisites

Before using this repository, ensure you have:

1. An AWS account with access to **Lambda, CloudWatch, and SNS**.
2. An IAM role with the necessary **permissions**.
3. An SNS topic configured for **email notifications**.

## 🚀 Installation & Setup

### Step 1: Deploy AWS Lambda Function
1. Go to **AWS Lambda** and create a new function.
2. Choose **Python 3.x** as the runtime.
3. Attach the required **IAM permissions**.

### Step 2: Set Up CloudWatch and SNS
1. Create a **CloudWatch log group** for your Lambda function.
2. Create a **CloudWatch metric filter** for error detection.
3. Configure an **SNS topic** for notifications.

### Step 3: Upload the Scripts
1. Place the **test error script** and **automatic error detection script** in your Lambda environment.
2. Refer to the [**`scripts/`**](./scripts/) directory in this repository for script details.

## 🔧 How to Test

1. **Deploy the Test Error Script (`test_error.py`)**  
   - Invoke the function manually to trigger an error.
   - Check **CloudWatch logs** to verify if the error is recorded.
  
2. **Deploy the Automatic Error Detection Script (`error_monitor.py`)**  
   - Ensure it detects errors **automatically**.
   - Verify that **SNS notifications** are received.

For detailed explanations, refer to the documentation in the [**`job-sheet/`**](./job-sheet/) folder.

Feel free to contribute to improve these playbooks or optimize the configurations!
