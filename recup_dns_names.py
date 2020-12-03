# This Python file uses the following encoding: utf-8
def recup_dns_names(client):
    dns_names = []
    ip_addresses = []
    instances = client.describe_instances()
    
    # Faire une boucle avec l'itérable que fournit instances pour recup tous les dns names de nos instances
    for i in range(len(instances['Reservations'])):
        for j in range(len(instances['Reservations'][i]['Instances'])):
            if instances['Reservations'][i]['Instances'][j]['State']['Name'] == 'running':
                dns_names.append(instances['Reservations'][i]['Instances'][j]['PublicDnsName'])
                ip_addresses.append(instances['Reservations'][i]['Instances'][j]['PublicIpAddress'])

    #print(dns_names)
    return [dns_names, ip_addresses]
    
    