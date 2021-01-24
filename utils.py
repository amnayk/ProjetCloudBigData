def is_pending(id_filter, ec2):
    reservations = ec2.describe_instances(Filters = id_filter)["Reservations"]
    for intances in reservations:
        for instance in intances['Instances']:
            if instance['State']['Name'] == 'pending':
                print("    "+str(instance['InstanceId'])+" is still "+instance["State"]["Name"]+"... (not checking others)")
                return True
            else:
                print("    "+str(instance['InstanceId'])+" is now "+instance["State"]["Name"]+"!")
    return False