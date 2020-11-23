from config_chanch import REGION_NAME, ACCESS_KEY, SECRET_KEY, EC2_KEY_PAIR
from botocore.exceptions import ClientError
from botocore.config import Config
import boto3
from os import chdir, getcwd
chdir(getcwd())


# 21 septembre

my_config = Config(
    region_name=REGION_NAME,
)

client = boto3.client('ec2',
                      config=my_config,
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY
                      )

# Clés SSH
outfile = open(EC2_KEY_PAIR + '.pem', 'w')
try:
    response = client.create_key_pair(
        KeyName=EC2_KEY_PAIR,
    )
    print(response)
    KeyPairOut = str(response['KeyMaterial'])
    outfile.write(KeyPairOut)
except ClientError:
    print("La clé existe déjà, essaye de stop.py")


ec2 = boto3.resource('ec2',
                     config=my_config,
                     aws_access_key_id=ACCESS_KEY,
                     aws_secret_access_key=SECRET_KEY)


ec2.create_instances(ImageId='ami-0d3f551818b21ed81',
                     InstanceType='t2.micro',
                     MinCount=1,
                     MaxCount=1,
                     )


response = client.describe_instances()
print(response)
