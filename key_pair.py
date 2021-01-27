import argparse
import boto3
import os
from botocore.config import Config
from private_config import ACCESS_KEY, SECRET_KEY, REGION_NAME, username
from botocore.exceptions import ClientError

DEFAULT_NAME = username+"_key"


def parse_arguments():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Generate keypair for EC2 instances so they can be accessed via SSH""",
    )

    parser.add_argument(
        "-c", "--create", help="Create key pair", action="store_true")

    parser.add_argument(
        "-d", "--delete", help="Delete key pair", action="store_true")

    parser.add_argument(
        "-l", "--list", help="list key pairs", action="store_true")

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


def create_key_pair(ec2, name=DEFAULT_NAME):

    # call the boto ec2 function to create a key pair
    try:
        key_pair = ec2.create_key_pair(KeyName=name)
    except ClientError:
        print("Key Pair already exists online. If you lost .pem file try delete.")
        return

    # create a file to store the key locally
    try:
        outfile = open(name + ".pem", "w")
    except PermissionError:
        print(name + ".pem already exists, modifying it")
        os.chmod(name + ".pem", 0o777)
        outfile = open(name + ".pem", "w")
    os.chmod(name + ".pem", 0o400)

    # capture the key and store it in a file
    KeyPairOut = key_pair["KeyMaterial"]
    # print(key_pair)
    print("Key Pair generated : " + name)
    outfile.write(KeyPairOut)
    return


def delete_keypair(ec2, name=DEFAULT_NAME):
    configured_keys = [key["KeyName"]
                       for key in ec2.describe_key_pairs()["KeyPairs"]]
    print("Deleting key : " + name)
    if name in configured_keys:
        ec2.delete_key_pair(KeyName=name)
        try:
            os.remove(name + ".pem")
        except PermissionError:
            print("Deleting locally failed (PermissionError), retrying..")
            os.chmod(name + ".pem", 0o777)
            os.remove(name + ".pem")
        print(name + ' deleted.')

    else:
        print("Key not found, try listing the keys")


def delete_keypair_all(ec2):
    configured_keys = [key["KeyName"]
                       for key in ec2.describe_key_pairs()["KeyPairs"]]
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

    my_config = Config(region_name=REGION_NAME)

    ec2 = boto3.client("ec2", config=my_config,
                       aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    if args.create:
        create_key_pair(ec2, args.name)
    elif args.delete:
        delete_keypair(ec2)
    elif args.list:
        list_keypairs(ec2)
