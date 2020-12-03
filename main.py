# This Python file uses the following encoding: utf-8
from lancer_k8s_ssh import lancer_k8s_ssh
from create_instances import create_instances
from create_security_group import create_security_group
from create_keys import create_keys
from recup_dns_names import recup_dns_names
import sys
from private_config import REGION_NAME, ACCESS_KEY, SECRET_KEY
from botocore.config import Config
import boto3
from os import chdir, getcwd
chdir(getcwd())


def main():

    my_config = Config(
        region_name=REGION_NAME,
    )

    ec2 = boto3.resource('ec2',
                         config=my_config,
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY)

    client = boto3.client('ec2',
                          config=my_config,
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)

    dns_names = []
    
    if len(sys.argv) == 1:
        print('Default')
        return 0
    else:
        cmd = sys.argv[1]
        args = sys.argv[2:]
        print(cmd, args)

    if cmd == 'ci':
        if args :
            print('Creation des instances')
            security_group = create_security_group(client, ec2)
            keys = create_keys(client)
            create_instances(ec2, security_group, keys, *args)
            return 0
        else :
            print("Veuillez ajouter un deuxième argument indiquant le nombre d'instances à lancer")

    # if cmd == 'ci':
    #     print('Creation des instances')
    #     create_instances(ec2, client, *args)
    #     return 0

    elif cmd == 'create_keys':
        print('Creation des clés')
        create_keys(client)
        return 0

    # elif cmd == 'create_security_group':
    #     print('Création du groupe de sécurité')
    #     create_security_group(client, ec2)
    #     return 0

    # elif cmd == 'recup_dns_names':
    #     print('Récupération des adresses IP de nos instances')
    #     dns_names = recup_dns_names(client)
    #     return 0

    elif cmd == 'launch_k8s':
        print('Récupération des adresses IP de nos instances')
        [dns_names, ip_adresses] = recup_dns_names(client)
        lancer_k8s_ssh(dns_names, ip_adresses)
        return 0

    else:
        print("Invalid argument : " + args[0])
        sys.exit(0)
        return 0


if __name__ == "__main__":
    main()
