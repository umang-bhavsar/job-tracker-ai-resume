import json
import boto3
import os
from botocore.exceptions import ClientError

#lets create the AWS clients
s3 = boto3.client('s3')                #to talk to amazon s3
textract = boto3.client('textract')    #to talk to amazon textract for extracting files  
dynamodb = boto3.client("dynamodb")    

def lambda_handler(event, context):
    print("Event:", json.dumps(event))

    try:
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        print(f"File uploaded: {object_key} in bucket: {bucket_name}")

        #extracting text
        response = textract.detect_document_text(
            Document = {'S3Object':{'Bucket': bucket_name, 'Name': object_key}}
        )
        extracted_text = ""
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                extracted_text += item['Text']+ "\n"
        
        print('Extracted text preview:', extracted_text[:300])

        f = open("sample-data/job_description.txt", "r")
        job_description = f.read()

        from utils.openai_handler import get_resume_score
        ai_result = get_resume_score(extracted_text, job_description)

        print("AI Scoring Result:", ai_result)

        return {
            'statusCode': 200,
            'body': f"Received file {object_key} from bucket {bucket_name}"
        }
    except Exception as e:
        print("Error extracting event info:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps("Failed to extract S3 event info")
        }
