# This Python file uses the following encoding: utf-8
def create_security_group(client, ec2):
    my_secu_group = client.create_security_group(
        Description='Security group for kubernetes deployment',
        GroupName='SNchos',
    )
    
    # Autoriser les requêtes ssh
    ec2.SecurityGroup(my_secu_group['GroupId']).authorize_ingress(
        CidrIp='0.0.0.0/0',
        FromPort=22,
        IpProtocol='tcp',
        ToPort=22,
    )

    return my_secu_group