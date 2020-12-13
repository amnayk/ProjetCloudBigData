from private_config import ACCESS_KEY, SECRET_KEY, REGION_NAME
import sys
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import argparse

DEFAULT_NAME = "sec_grp"
DEFAULT_DESC = "Security group with ssh permission"


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
        default=DEFAULT_DESC,
        dest="desc",
    )

    args = parser.parse_args()

    return args


def create_security_group(ec2, ec2_resource, name=DEFAULT_NAME, description=DEFAULT_DESC):
    # get VPCs
    response = ec2.describe_vpcs()
    vpc_id = response.get("Vpcs", [{}])[0].get("VpcId", "")

    # get already configured security groups
    response = ec2.describe_security_groups()
    security_groups = [grp["GroupName"]
                       for grp in response["SecurityGroups"]]
    print("Found", security_groups, "online.")

    # return the security group if it already exists
    if name in security_groups:
        print(name + " already created, returning it instead.")
        security_group = response["SecurityGroups"][security_groups.index(
            name)]
        security_group_id = security_group["GroupId"]

    # create it if it doesn't
    else:
        security_group = ec2.create_security_group(
            GroupName=name, Description=description, VpcId=vpc_id
        )

        security_group_id = security_group["GroupId"]
        print("Security group created %s in vpc %s (%s)." %
              (security_group_id, vpc_id, name))

        # Only allow ssh connections
        ec2_resource.SecurityGroup(security_group_id).authorize_ingress(
            CidrIp='0.0.0.0/0',
            # FromPort=22,
            # IpProtocol='tcp',
            IpProtocol='-1'
            # ToPort=22,
        )

    return security_group


def delete_security_groups(ec2):
    print("Deleting Security groups...\n")
    response = ec2.describe_security_groups()
    print("Found", [grp["GroupName"]
                    for grp in response["SecurityGroups"]], "\n")
    deleted = 0
    for grp in response["SecurityGroups"]:
        if grp["GroupName"] != "default":
            ec2.delete_security_group(
                GroupId=grp["GroupId"],
            )
            print("Deleted the group : " + grp["GroupName"])
            deleted += 1
        else:
            print("Skipping 'default'")
    print("\nDeleted", deleted, "groups.")


if __name__ == "__main__":
    args = parse_arguments()

    my_config = Config(region_name=REGION_NAME)

    ec2 = boto3.client("ec2", config=my_config,
                       aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    ec2_res = boto3.resource("ec2", config=my_config,
                             aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    if args.create:
        create_security_group(ec2, ec2_res, args.name, args.desc)
    elif args.delete:
        delete_security_groups(ec2)
