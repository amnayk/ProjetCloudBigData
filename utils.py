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

def is_checking(ids, ec2):
    reservations = ec2.describe_instance_status(InstanceIds = ids)['InstanceStatuses']
    for status in reservations:
        if status['InstanceStatus']['Status'] != 'ok' or status['SystemStatus']['Status'] != 'ok':
            print("    "+str(status['InstanceId'])+" : InstanceStatus or SystemStatus is still initializing ... (not checking others)")
            return True
        else:
            print("    "+str(status['InstanceId'])+" is now " + status["InstanceStatus"]["Status"]+" !")
    return False