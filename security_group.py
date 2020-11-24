from private_config import REGION_NAME, ACCESS_KEY, SECRET_KEY, EC2_KEY_PAIR
from botocore.exceptions import ClientError
from botocore.config import Config
import boto3
from os import chdir, getcwd
chdir(getcwd())

my_config = Config(
    region_name=REGION_NAME,
)

client = boto3.client('ec2',
                      config=my_config,
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY
                      )

client.create_security_group(
    Description='Security group for kubernetes deployment',
    GroupName='SNchos',
    VpcId='vpc-79c02b11'
)
