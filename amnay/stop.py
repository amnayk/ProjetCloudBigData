from private_config import ACCESS_KEY, SECRET_KEY
import argparse
import boto3
from botocore.exceptions import ClientError

from key_pair import delete_keypair, delete_keypair_all
from security_group import delete_security_groups
import time


def terminate_instances():

    ec2_res = boto3.resource(
        "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )
    try:
        response = ec2_res.instances.terminate()[0]["TerminatingInstances"]
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
    except Exception as e:
        print(e)


if __name__ == "__main__":

    ec2 = boto3.client(
        "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )

    delete_keypair_all(ec2)

    terminate_instances()

    time.sleep(30)

    delete_security_groups(ec2)
