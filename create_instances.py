def create_instances(resource, count, ImageId='ami-0d3f551818b21ed81', InstanceType='t2.micro'):
    id_instance = resource.create_instances(ImageId=ImageId,
                                         InstanceType=InstanceType,
                                         MinCount=int(count),
                                         MaxCount=int(count),
                                         )
    print(id_instance)
    
    ip_instance = resource.Instance(id_instance).public_ip_address

    print(ip_instance)
# ssh -i cle.pem root@[IP]  `commande shell`
