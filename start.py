import boto3
from botocore.config import Config

# 21 septembre

REGION_NAME = "eu-west-3"
ACCESS_KEY = "AKIAJIKROG7ETHURCNBQ"
SECRET_KEY = "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"

my_config = Config(
    region_name=REGION_NAME,
)

client = boto3.client('ec2',
                      config=my_config,
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY
                      )
