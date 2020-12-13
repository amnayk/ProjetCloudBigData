from botocore.exceptions import ClientError


def create_keys(client, EC2_KEY_PAIR):
    outfile = open(EC2_KEY_PAIR + '.pem', 'w')
    try:
        response = client.create_key_pair(
            KeyName=EC2_KEY_PAIR
        )
        print(response)
        KeyPairOut = str(response['KeyMaterial'])
        outfile.write(KeyPairOut)
    except ClientError:
        print("La clé existe déjà, essaye de stop.py")
