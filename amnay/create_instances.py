def create_instances(ec2_resource, sg_id, NUMBER_NODES, USER):
    instances = ec2_resource.create_instances(
        ImageId="ami-0d3f551818b21ed81",
        MinCount=1,
        MaxCount=NUMBER_NODES,
        InstanceType="t2.micro",
        KeyName=USER,
        SecurityGroupIds=[str(sg_id)],
    )
    return instances