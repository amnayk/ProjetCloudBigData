from private_config import REGION_NAME, ACCESS_KEY, SECRET_KEY, EC2_KEY_PAIR
from botocore.exceptions import ClientError
from botocore.config import Config
import boto3
from os import chdir, getcwd
chdir(getcwd())


# 21 septembre

my_config = Config(
    region_name=REGION_NAME,
)

ec2 = boto3.resource('ec2',
                     config=my_config,
                     aws_access_key_id=ACCESS_KEY,
                     aws_secret_access_key=SECRET_KEY)


ec2.create_instances(ImageId='ami-0d3f551818b21ed81',
                     InstanceType='t2.micro',
                     MinCount=1,
                     MaxCount=1,
                     )
