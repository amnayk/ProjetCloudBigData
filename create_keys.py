from private_config import EC2_KEY_PAIR
from botocore.exceptions import ClientError

def create_keys(client, ec2_key = EC2_KEY_PAIR):
    # Clés SSH
    outfile = open(ec2_key + '.pem', 'w')
    try:
        response = client.create_key_pair(
            KeyName=ec2_key
        )
        print(response)
        KeyPairOut = str(response['KeyMaterial'])
        outfile.write(KeyPairOut)
    except ClientError:
        print("La clé existe déjà, essaye de stop.py")
