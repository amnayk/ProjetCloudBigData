# This Python file uses the following encoding: utf-8
from private_config import EC2_KEY_PAIR
def create_instances(resource, security_group, keys, count, ImageId='ami-0d3f551818b21ed81', InstanceType='t2.micro'):
    instances = resource.create_instances(ImageId=ImageId,
                                         InstanceType=InstanceType,
                                         KeyName=keys["KeyName"],
                                         MaxCount=int(count),
                                         MinCount=int(count),
                                         NetworkInterfaces=[{'AssociatePublicIpAddress' : True, 'DeviceIndex' : 0}]
                                         )
                                         
    for instance in instances: 
        resource.Instance(instance.id).modify_attribute(
            Groups=[security_group["GroupId"]]
        )

    return 0