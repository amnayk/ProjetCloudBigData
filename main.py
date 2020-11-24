from create_instances import create_instances
from create_security_group import create_security_group
from create_keys import create_keys
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

    if len(sys.argv) == 1:
        print('Default')
        return 0
    else:
        cmd = sys.argv[1]
        args = sys.argv[2:]
        print(cmd, args)

    if cmd == 'ci':
        print('Creation des instances')
        create_instances(ec2, *args)
        return 0

    elif cmd == 'create_keys':
        print('Creation des clés')
        create_keys(client)
        return 0

    elif cmd == 'create_security_group':
        print('Creation du groupe de sécurité')
        create_security_group(client)
        return 0

    else:
        print("Invalid argument : " + args[0])
        sys.exit(0)
        return 0


if __name__ == "__main__":
    main()
