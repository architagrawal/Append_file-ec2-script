# Script to Process on EC2- 

This Script is responsible for getting the data from DynamoDB, download the input file from S3 to /tmp file, appending the input text to the input file, uploading the new file to output s3 and entering a new item in DynamoDB with the same ID as input file's ID and a path to output file in s3.

## Run Locally

1. Clone the project

```bash
  git clone https://github.com/architagrawal/fovus-ec2-script.git
```
2. Replace the Access and Secret Keys in script for the IAM role that has write access to s3 and DynamoDB. 

2. Upload the .py file to s3 bucket

