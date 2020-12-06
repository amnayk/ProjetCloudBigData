import paramiko

def lancer_k8s_ssh(CLUSTER, USER):
    k = paramiko.RSAKey.from_private_key_file(USER + '.pem')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("ssh.log")
    # Lancement de k8s sur les master nodes
    for master in CLUSTER["Masters"]:
        ssh.connect(hostname=master["Dns_Name"], username='ubuntu', pkey=k)
        ssh.exec_command('sudo apt-get update -y')
        ssh.exec_command('sudo hostnamectl set-hostname master')
        ssh.exec_command('echo "' + master["Ip_Address"] + '   master" | sudo tee -a /etc/hosts')
        
        
        # Pour afficher la sortie standard sur notre sortie standard de la vm cible
        # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cat /etc/hosts')
        # for line in iter(ssh_stdout.readline, ""):
        #     print(line)
        # for line2 in iter(ssh_stderr.readline, ""):
        #     print(line2)

    # Lancement de k8s sur les slave nodes
    # ssh.exec_command('echo "' + + '   slave" | sudo tee -a /etc/hosts')
        
    return 0