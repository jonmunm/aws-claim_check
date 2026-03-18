# AWS Claim Check Pattern Implementation

### Description
This project implements the **Claim Check** pattern on AWS to handle large data payloads. Instead of sending heavy data directly through a message queue, it stores the content in **Amazon S3** and sends a small reference (pointer) to the consumer via **Amazon SQS**. This architecture ensures system reliability, reduces messaging overhead, and bypasses the 256 KB limit of SQS.

---

## 🛠 Infrastructure Components
The infrastructure is managed via **AWS SAM (Serverless Application Model)** and includes:
* **Amazon S3:** The persistent store for large message payloads.
* **Amazon SQS:** Standard queue for lightweight claims (pointers).
* **AWS Lambda:** Serverless compute for processing logic (Python 3.11).
* **Amazon CloudWatch:** Centralized monitoring for infrastructure logs and custom performance metrics.
* **IAM Roles:** Fine-grained permissions for secure inter-service communication.

---

## 🏗 Technical Architecture
1. **Producer:** Uploads large files to the S3 Bucket and sends a small JSON message to the SQS Queue containing the S3 Object Key.
2. **Messaging:** SQS triggers the AWS Lambda function automatically upon receiving the claim message.
3. **Consumer (Lambda):** Retrieves the S3 Key from the message, downloads the full payload from S3, and executes the business logic. It then publishes custom metrics to CloudWatch.

![Design](amazon.gif)

---

## 🚀 Getting Started

### 1. Prerequisites
* [AWS CLI](https://aws.amazon.com/cli/) configured with proper credentials.
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) installed.
* [Python 3.11+](https://www.python.org/downloads/)

### 2. Clone the Repository
```bash
git clone https://github.com/jonmunm/aws-claim_check.git
cd aws-claim_check
```

### 3. Deploy Infrastructure (AWS SAM)
The deployment is fully automated. The template.yaml includes a **DeploymentId** parameter to uniquely identify your resources.

```bash
# Build the application
sam build

# Deploy the stack
sam deploy --guided --parameter-overrides DeploymentId="<YOUR_ID>"
```

*Note: During the guided deploy, ensure you provide the DeploymentID to act as a suffix for AWS resources.*

### 4. Local Development & Testing
You can invoke the Lambda function locally using a mock SQS event:

```bash
# Generate a sample SQS event
sam local generate-event sqs receive-message --body '{"s3_key": "large_file.csv"}' > event.json

# Invoke the function locally
sam local invoke "ClaimCheckFunction" -e event.json
```

📖 Reference Documentation
1. [AWS Architecture Blog: Handling large payloads in SQS](https://learn.microsoft.com/en-us/azure/architecture/patterns/claim-check)
1. [Enterprise Integration Patterns: Claim Check](https://www.enterpriseintegrationpatterns.com/patterns/messaging/StoreInLibrary.html)
