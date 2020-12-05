from private_config import ACCESS_KEY, SECRET_KEY
import boto3
from botocore.exceptions import ClientError
import argparse

DEFAULT_NAME = "sec_grp"


def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Create security group (SG)""",
    )

    parser.add_argument(
        "-c", "--create", help="Create Security Group", action="store_true"
    )

    parser.add_argument(
        "-d", "--delete", help="Delete Security Group", action="store_true"
    )

    parser.add_argument(
        "-n",
        "--name",
        help="Name of Security Group",
        type=str,
        default=DEFAULT_NAME,
        dest="name",
    )

    parser.add_argument(
        "--desc",
        help="Description",
        default="Security group",
        dest="desc",
    )

    args = parser.parse_args()

    return args


def create_security_group(ec2, ec2_resource, name, description):
    response = ec2.describe_vpcs()
    vpc_id = response.get("Vpcs", [{}])[0].get("VpcId", "")
    try:
        security_group = ec2.create_security_group(
            GroupName=name, Description=description, VpcId=vpc_id
        )

        security_group_id = security_group["GroupId"]
        print("Security Group Created %s in vpc %s (%s)." % (security_group_id, vpc_id, name))
        
        # Autoriser uniquement les requêtes ssh
        ec2_resource.SecurityGroup(security_group_id).authorize_ingress(
            CidrIp='0.0.0.0/0',
            FromPort=22,
            IpProtocol='tcp',
            ToPort=22,
        )

    
    except ClientError as e:
        print(e)

    return security_group


def delete_security_groups(ec2):
    response = ec2.describe_security_groups()
    for grp in response["SecurityGroups"]:
        if grp["GroupName"] != "default":
            ec2.delete_security_group(
                GroupId=grp["GroupId"],
            )
            print("Deleted the group : " + grp["GroupName"])


if __name__ == "__main__":
    args = parse_arguments()

    ec2 = boto3.client(
        "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )

    if args.create:
        create_security_group(ec2, args.name, args.desc)
    elif args.delete:
        delete_security_groups(ec2)