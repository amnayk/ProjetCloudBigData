def recup_dns_names_and_ip(client):
    dns_names_master = []
    dns_names_slave = []
    ip_addresses_master = []
    ip_addresses_slave = []

    instances = client.describe_instances()
    
    # Faire une boucle avec l'itérable que fournit instances pour recup tous les dns names de nos instances
    for i in range(len(instances['Reservations'])):
        for j in range(len(instances['Reservations'][i]['Instances'])):
            if instances['Reservations'][i]['Instances'][j]['State']['Name'] == 'running':
                if instances['Reservations'][i]['Instances'][j]['Tags'][0]['Value'] == 'Master':
                    dns_names_master.append(instances['Reservations'][i]['Instances'][j]['PublicDnsName'])
                    ip_addresses_master.append(instances['Reservations'][i]['Instances'][j]['PublicIpAddress'])
                else:
                    dns_names_slave.append(instances['Reservations'][i]['Instances'][j]['PublicDnsName'])
                    ip_addresses_slave.append(instances['Reservations'][i]['Instances'][j]['PublicIpAddress'])


    return [dns_names_master, ip_addresses_master, dns_names_slave, ip_addresses_slave]
    