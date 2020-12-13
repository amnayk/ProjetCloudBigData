def create_instances(ec2_resource, security_group, NUMBER_WORKERS, NUMBER_MASTERS, USER):
    master_instances = ec2_resource.create_instances(
        ImageId="ami-0d3f551818b21ed81",
        MinCount=1,
        MaxCount=NUMBER_MASTERS,
        InstanceType="t2.micro",
        KeyName=USER,
        NetworkInterfaces=[{'AssociatePublicIpAddress': True, 'DeviceIndex' : 0}],
        TagSpecifications=[{'ResourceType': "instance", 'Tags':[{'Key': "Type", 'Value': "Master"}]}]
    )

    slave_instances = ec2_resource.create_instances(
        ImageId="ami-0d3f551818b21ed81",
        MinCount=1,
        MaxCount=NUMBER_WORKERS,
        InstanceType="t2.micro",
        KeyName=USER,
        NetworkInterfaces=[{'AssociatePublicIpAddress' : True, 'DeviceIndex' : 0}],
        TagSpecifications=[{'ResourceType': "instance", 'Tags':[{'Key': "Type", 'Value': "Slave"}]}]
    )

    for instance in [slave_instances, master_instances]: 
        ec2_resource.Instance(instance[0].id).modify_attribute(
            Groups=[security_group["GroupId"]]
        )

    return [master_instances, slave_instances]