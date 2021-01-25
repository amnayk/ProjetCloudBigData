from private_config import ACCESS_KEY, SECRET_KEY, username, REGION_NAME

import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=REGION_NAME):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        region_name=region,
        aws_secret_access_key=SECRET_KEY,
    )
    location = {"LocationConstraint": region}
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    print("Bucket created successfully")

    return True


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client(
        "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False


# create_bucket("sanchoss")

# uploaded = upload_to_aws("wordcount/filesample.txt", "sanchoss", "filesample.txt")

