# This Python file uses the following encoding: utf-8
from os import stat
from private_config import EC2_KEY_PAIR
from botocore.exceptions import ClientError
import os

def create_keys(client, ec2_key = EC2_KEY_PAIR):
    # Clés SSH
    outfile = open(ec2_key + '.pem', 'w')
    os.chmod(ec2_key + '.pem', 0o400)
    try:
        response = client.create_key_pair(
            KeyName=ec2_key
        )
        print(response)
        KeyPairOut = str(response['KeyMaterial'])
        outfile.write(KeyPairOut)
    except ClientError:
        print("La clé existe déjà, essaye de stop.py")
    return response
