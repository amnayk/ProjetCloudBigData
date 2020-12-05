import paramiko

def lancer_k8s_ssh(dns_names, ip_adresses, USER):
    k = paramiko.RSAKey.from_private_key_file(USER + '.pem')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("ssh.log")
    for i in range (len(dns_names)):
        ssh.connect(hostname=dns_names[i], username='ubuntu', pkey=k)
        ssh.exec_command('sudo apt-get update -y')
        ssh.exec_command('sudo hostnamectl set-hostname master')
        ssh.exec_command('echo "' + ip_adresses[i] + '   master" | sudo tee -a /etc/hosts')
        # ssh.exec_command('echo "' + + '   slave" | sudo tee -a /etc/hosts')
        
        # Pour afficher la sortie standard sur notre sortie standard de la vm cible
        # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cat /etc/hosts')
        # for line in iter(ssh_stdout.readline, ""):
        #     print(line)
        # for line2 in iter(ssh_stderr.readline, ""):
        #     print(line2)
        
    return 0