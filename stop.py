from private_config import REGION_NAME, ACCESS_KEY, SECRET_KEY, EC2_KEY_PAIR
from botocore.exceptions import ClientError
from botocore.config import Config
import boto3
from os import chdir, getcwd, remove

chdir(getcwd())

my_config = Config(
    region_name=REGION_NAME,
)

client = boto3.client(
    "ec2",
    config=my_config,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)
ec2 = boto3.resource(
    "ec2",
    config=my_config,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

# Deleting SSH key pairs
configured_keys = [key["KeyName"] for key in client.describe_key_pairs()["KeyPairs"]]
for keyName in configured_keys:
    print("Deleteing key : " + keyName)
    client.delete_key_pair(KeyName=keyName)
    remove(keyName + ".pem")
print("Deleted " + str(len(configured_keys)) + " keys.\n")

# Removing instances
response = ec2.instances.terminate()[0]["TerminatingInstances"]
response = [
    status
    for status in response
    if status["PreviousState"]["Name"] != status["CurrentState"]["Name"]
]
for status in response:
    print(
        status["InstanceId"]
        + " : "
        + status["PreviousState"]["Name"]
        + " -> "
        + status["CurrentState"]["Name"]
    )
print("Terminated " + str(len(response)) + " instances.\n")
