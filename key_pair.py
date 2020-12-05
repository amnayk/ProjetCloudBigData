import argparse
import boto3
import os
from private_config import ACCESS_KEY, SECRET_KEY
from botocore.exceptions import ClientError

DEFAULT_NAME = "user_keypair"


def parse_arguments():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Generate keypair for EC2 instances so they can be accessed via SSH""",
    )

    parser.add_argument("-c", "--create", help="Create key pair", action="store_true")

    parser.add_argument("-d", "--delete", help="Delete key pair", action="store_true")

    parser.add_argument("-l", "--list", help="list key pairs", action="store_true")

    parser.add_argument(
        "-n",
        "--name",
        help="Key pair's name",
        type=str,
        default=DEFAULT_NAME,
        dest="name",
    )

    args = parser.parse_args()

    return args


def create_key_pair(ec2, name):
    # create a file to store the key locally
    outfile = open(name + ".pem", "w")
    os.chmod(name + ".pem", 0o400)

    try:
        # call the boto ec2 function to create a key pair
        key_pair = ec2.create_key_pair(KeyName=name)
        # capture the key and store it in a file
        KeyPairOut = key_pair["KeyMaterial"]
        # print(key_pair)
        print("Key Pair generated : " + name)
        outfile.write(KeyPairOut)
    except ClientError as identifier:
        print("Key Pair already exists, try delete")


def delete_keypair(ec2, name):
    configured_keys = [key["KeyName"] for key in ec2.describe_key_pairs()["KeyPairs"]]
    if name in configured_keys:
        print("Deleteing key : " + name)
        ec2.delete_key_pair(KeyName=name)
        os.remove(name + ".pem")
    else:
        print("Key not found, try listing the keys")


def delete_keypair_all(ec2):
    configured_keys = [key["KeyName"] for key in ec2.describe_key_pairs()["KeyPairs"]]
    for name in configured_keys:
        print("Deleting key : " + name)
        ec2.delete_key_pair(KeyName=name)
        try:
            os.remove(name + ".pem")
        except FileNotFoundError:
            pass


def list_keypairs(ec2):
    if len(ec2.describe_key_pairs()["KeyPairs"]) == 0:
        print("No keys found")
    else:
        for key in ec2.describe_key_pairs()["KeyPairs"]:
            print(key["KeyName"])


if __name__ == "__main__":

    args = parse_arguments()

    ec2 = boto3.client(
        "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )

    if args.create:
        create_key_pair(ec2, args.name)
    elif args.delete:
        delete_keypair(ec2, args.name)
    elif args.list:
        list_keypairs(ec2)