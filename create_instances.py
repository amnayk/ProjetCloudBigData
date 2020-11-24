def create_instances(resource, count=1, ImageId='ami-0d3f551818b21ed81', InstanceType='t2.micro'):
    response = resource.create_instances(ImageId=ImageId,
                                         InstanceType=InstanceType,
                                         MinCount=int(count),
                                         MaxCount=int(count),
                                         )
    print(response)
# ssh -i cle.pem root@[IP]  `commande shell`
