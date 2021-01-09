import time
from private_config import ACCESS_KEY, SECRET_KEY, username, REGION_NAME
import argparse
import boto3
from botocore.exceptions import ClientError

from key_pair import create_key_pair
from security_group import create_security_group
from create_instances import create_instances
from cluster_k8s_ssh import lancer_k8s_ssh

DEFAULT_NUMBER_MASTERS = 1
DEFAULT_NUMBER_WORKERS = 2

USER = None
NUMBER_MASTERS = None
NUMBER_WORKERS = None
NUMBER_NODES = None
KEY_NAME = None
SECURITY_GROUP = "lessanchos"
SECURITY_GROUP_DESC = "Pour notre cluster K8s"

CLUSTER = {"Masters": [], "Slaves": []}


def parse_arguments():

    global USER, KEY_NAME, NUMBER_MASTERS, NUMBER_WORKERS, NUMBER_NODES

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Create an AWS cluster and deploy kubernetes in it""",
    )

    parser.add_argument(
        "-u",
        "--user",
        dest="user",
        type=str,
        default=username,
        help="Specify a username",
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

    USER = args.user or username
    KEY_NAME = USER + '_key'
    NUMBER_MASTERS = args.nb_masters or DEFAULT_NUMBER_MASTERS
    NUMBER_WORKERS = args.nb_workers or DEFAULT_NUMBER_WORKERS
    NUMBER_NODES = NUMBER_MASTERS + NUMBER_WORKERS

    print("Deploying cluster with the following parameters : ")
    print(vars(args))


if __name__ == "__main__":

    parse_arguments()

    ec2 = boto3.client(
        "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION_NAME,
    )

    ec2_resource = boto3.resource(
        "ec2", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION_NAME
    )

    # Key pairs
    print("\nGenerating keypairs")
    try:
        create_key_pair(ec2, name=USER+"_key")
    except Exception as e:
        print(e)

    # Security groups
    print("\nGenerating security group : " + SECURITY_GROUP)
    security_group = create_security_group(
        ec2, ec2_resource, name=SECURITY_GROUP, description=SECURITY_GROUP_DESC)

    [master_instances, slave_instances] = create_instances(
        ec2_resource, security_group, NUMBER_WORKERS, NUMBER_MASTERS, KEY_NAME)

    print("\nLaunching instances ...")

    # Il faut le temps que les instances soient créées et dans l'état "running"
    time.sleep(180)

    # Remplissage du dictionnaire permettant de centraliser les infos sur les slaves et masters
    for instance in master_instances:
        CLUSTER["Masters"].append(
            {
                "Id_Instance": instance.id,
                "Ip_Address": ec2_resource.Instance(instance.id).public_ip_address,
                "Dns_Name": ec2_resource.Instance(instance.id).public_dns_name
            }
        )

    num_slave = 1
    for instance in slave_instances:
        CLUSTER["Slaves"].append(
            {
                "Id_Slave": "slave" + str(num_slave),
                "Id_Instance": instance.id,
                "Ip_Address": ec2_resource.Instance(instance.id).public_ip_address,
                "Dns_Name": ec2_resource.Instance(instance.id).public_dns_name
            }
        )
        num_slave += 1

    # Lancement du cluster K8s
    print("\nLaunching the k8s cluster on : " + str(CLUSTER))
    lancer_k8s_ssh(CLUSTER, KEY_NAME)
