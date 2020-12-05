import time
from private_config import ACCESS_KEY, SECRET_KEY
import argparse
import boto3
from botocore.exceptions import ClientError

from key_pair import create_key_pair
from security_group import create_security_group
from create_instances import create_instances
from dns_ip_address import recup_dns_names_and_ip
from cluster_k8s_ssh import lancer_k8s_ssh

DEFAULT_USER = "amnay"
DEFAULT_REGION = "eu-west-3"
DEFAULT_NUMBER_MASTERS = 1
DEFAULT_NUMBER_WORKERS = 2

USER = None
REGION = None
NUMBER_MASTERS = None
NUMBER_WORKERS = None
NUMBER_NODES = None
SECURITY_GROUP = None

# CLUSTER = {"Masters": []}
# CLUSTER["Masters"]["addIPublic"]


def parse_arguments():

    global USER
    global REGION
    global NUMBER_MASTERS
    global NUMBER_WORKERS
    global NUMBER_NODES
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Create an AWS cluster and deploy kubernetes in it""",
    )

    parser.add_argument(
        "-u",
        "--user",
        dest="user",
        type=str,
        default=DEFAULT_USER,
        help="Specify a username",
    )
    parser.add_argument(
        "-r",
        "--region",
        dest="region",
        type=str,
        default=DEFAULT_REGION,
        help="Specify the region where the cluster will be deployed",
    )

    parser.add_argument(
        "-m",
        "--masters",
        dest="nb_masters",
        type=int,
        default=DEFAULT_NUMBER_MASTERS,
        help="Specify the number of masters",
    )

    parser.add_argument(
        "-w",
        "--workers",
        dest="nb_workers",
        type=int,
        default=DEFAULT_NUMBER_WORKERS,
        help="Specify the number of workers",
    )

    args = parser.parse_args()

    USER = args.user
    REGION = args.region
    NUMBER_MASTERS = args.nb_masters
    NUMBER_WORKERS = args.nb_workers
    NUMBER_NODES = NUMBER_MASTERS + NUMBER_WORKERS

    print("Deploying cluster with the following parameters : ")
    print(vars(args))


if __name__ == "__main__":

    parse_arguments()

    ec2 = boto3.client(
        "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION,
    )

    ec2_resource = boto3.resource(
        "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION
    )

    create_key_pair(ec2, name=USER)

    security_group = create_security_group(ec2, ec2_resource, name="lessanchos", description="Pour notre cluster K8s")

    instances = create_instances(ec2_resource, security_group, NUMBER_NODES, USER)

    # Il faut le temps que les instances soient créées et dans l'état "running"
    time.sleep(20)
    [dns_names, ip_adresses] = recup_dns_names_and_ip(ec2)

    lancer_k8s_ssh(dns_names, ip_adresses, USER)




