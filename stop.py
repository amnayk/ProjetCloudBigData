from os import remove
from os.path import isfile
from private_config import ACCESS_KEY, SECRET_KEY, username, REGION_NAME
import boto3

from key_pair import delete_keypair_all, delete_keypair
from security_group import delete_security_groups
import time
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Create security group (SG)""",
    )

    parser.add_argument(
        "-me", "--me", help="Stops the cluster I created", action="store_true"
    )

    args = parser.parse_args()

    return args


def terminate_instances(Filters):

    try:
        ec2_res = boto3.resource(
            "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION_NAME
        )

        response = ec2_res.instances.filter(Filters=Filters).terminate()

        if response:
            TerminatingInstances = response[0]["TerminatingInstances"]

            print("Found " + str(len(TerminatingInstances)) + " instances.")
            for instance in TerminatingInstances:
                print(
                    "    "
                    + instance["InstanceId"]
                    + " : "
                    + instance["PreviousState"]["Name"]
                    + " -> "
                    + instance["CurrentState"]["Name"]
                )

            statuses = [
                status
                for status in TerminatingInstances
                if status["PreviousState"]["Name"] != "terminated"
            ]
            print("Found " + str(len(statuses)) + " instances to terminate.")

            print("Terminated " + str(len(statuses)) + " instances.\n")
        else:
            print("Nothing to terminate")

    except Exception as e:
        print(e)


if __name__ == "__main__":

    args = parse_arguments()

    ec2 = boto3.client(
        "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION_NAME
    )

    key_name = username+"_key"

    if args.me:
        print("Stopping using "+key_name)
        Filters = [
            {
                'Name': 'key-name',
                'Values': [
                    key_name
                ]
            }
        ]
    else:
        print("Stopping everything")
        Filters = []

    # Instances
    terminate_instances(Filters)

    # Keypairs
    if args.me:
        delete_keypair(ec2, key_name)
    else:
        delete_keypair_all(ec2)

    # Security groups
    if len(ec2.describe_security_groups()['SecurityGroups']) > 1 and not args.me:
        delete_security_groups(ec2)

    # Remove ssh.log
    if isfile("ssh.log"):
        remove("ssh.log")
        print("Deleted file ssh.log")
