def create_instances(ec2_resource, security_group, NUMBER_NODES, USER):
    instances = ec2_resource.create_instances(
        ImageId="ami-0d3f551818b21ed81",
        MinCount=1,
        MaxCount=NUMBER_NODES,
        InstanceType="t2.micro",
        KeyName=USER,
        NetworkInterfaces=[{'AssociatePublicIpAddress' : True, 'DeviceIndex' : 0}]
    )

    for instance in instances: 
        ec2_resource.Instance(instance.id).modify_attribute(
            Groups=[security_group["GroupId"]]
        )

    return instances