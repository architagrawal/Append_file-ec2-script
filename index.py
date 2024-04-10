import boto3
import os
import sys
from botocore.exceptions import ClientError
aws_access_key_id = "AKIA47CR2H7SRPE3KONT"
aws_secret_access_key = "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"
s3 = boto3.client('s3',aws_access_key_id= aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name="us-east-1")
dynamodb = boto3.resource('dynamodb', aws_access_key_id= aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name="us-east-1")

def download_file_from_s3(bucket_name, key, local_file_path):
    
    try:
        s3.download_file(bucket_name, key, local_file_path)
        print(f"File downloaded from S3: {local_file_path}")
        return True
    except ClientError as e:
        print(f"Error downloading file from S3: {e}")
        return False

def upload_file_to_s3(local_file_path, bucket_name, key):
    try:
        s3.upload_file(local_file_path, bucket_name, key)
        print(f"File uploaded to S3: s3://{bucket_name}/{key}")
        return True
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        return False

def append_text_to_file(input_text, input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        file_content = file.read()
    
    output_content = f"{file_content} : {input_text}"
    
    with open(output_file_path, 'w') as file:
        file.write(output_content)
    
    print(f"Output file created: {output_file_path}")

def main():

    file_table = dynamodb.Table('archit-db')
    output_table = dynamodb.Table('archit-db-out')
    itemId = sys.argv[1]
    # Step a: Get inputs from DynamoDB
    response = file_table.get_item(Key={'id': itemId})
    item = response.get('Item')
    if not item:
        print("Item not found in DynamoDB")
        return
    
    input_text = item.get('input_text')
    input_file_path = item.get('input_file_path')
    input_file_key = input_file_path.split('/')[1]
    print(input_text, input_file_key)
    output_file_key = f"Out-{os.path.basename(input_file_key)}"
    
    # Step b: Download input file from S3
    local_input_file_path = '/tmp/input.txt'
    if not download_file_from_s3('archit-fovus', input_file_key, local_input_file_path):
        return
    
    # Step c: Append text to input file
    local_output_file_path = '/tmp/output.txt'
    append_text_to_file(input_text, local_input_file_path, local_output_file_path)
    
    # Step d: Upload output file to S3
    if not upload_file_to_s3(local_output_file_path, 'archit-fovus-out', output_file_key):
        return
    
    # Step e: Save outputs and S3 path in DynamoDB
    try:
        output_table.put_item(Item={'id': itemId, 'output_file_path': f"archit-fovus-out/{output_file_key}"})
        print("Output saved to DynamoDB")
    except ClientError as e:
        print(f"Error saving output to DynamoDB: {e}")

if __name__ == "__main__":
    main()
