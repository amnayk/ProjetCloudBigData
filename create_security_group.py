def create_security_group(client):
    client.create_security_group(
        Description='Security group for kubernetes deployment',
        GroupName='SNchos',
        VpcId='vpc-79c02b11'
    )
