import time
from boto3 import NullHandler
import paramiko

def lancer_k8s_ssh(CLUSTER, USER):
    k = paramiko.RSAKey.from_private_key_file(USER + '.pem')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("ssh.log")

    for vm in [CLUSTER["Masters"], CLUSTER["Slaves"]]:
        ssh.connect(hostname=vm[0]["Dns_Name"], username='ubuntu', pkey=k)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo apt-get update -y')
        for line in iter(ssh_stdout.readline, ""):
            pass
        ssh.exec_command('swapoff -a')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo wget -qO- https://get.docker.com/ | sh')
        for line in iter(ssh_stdout.readline, ""):
            pass
        ssh.exec_command('sudo modprobe br_netfilter')
        ssh.exec_command('echo "net.bridge.bridge-nf-call-ip6tables = 1\nnet.bridge.bridge-nf-call-iptables = 1" | sudo tee -a /etc/sysctl.d/k8s.conf')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo sysctl --system')
        for line in iter(ssh_stdout.readline, ""):
            pass
        ssh.exec_command('curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')
        #ssh.exec_command('echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"')
        for line in iter(ssh_stdout.readline, ""):
            pass
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo apt-get update')
        for line in iter(ssh_stdout.readline, ""):
            pass
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('yes | sudo apt-get install kubelet kubeadm kubectl')
        for line in iter(ssh_stdout.readline, ""):
            pass  

    cmd_slave = ""
    
    # Lancement de k8s sur les master nodes
    for master in CLUSTER["Masters"]:
        ssh.connect(hostname=master["Dns_Name"], username='ubuntu', pkey=k)
        ssh.exec_command('sudo hostnamectl set-hostname master')
        ssh.exec_command('echo "' + master["Ip_Address"] + '   master" | sudo tee -a /etc/hosts')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo kubeadm init --ignore-preflight-errors=NumCPU --pod-network-cidr=10.0.0.0/16')
        for line in iter(ssh_stdout.readline, ""):
            if line[0:7] == "kubeadm":
                cmd_slave = line[0:len(line)-2]
            if line[0:6] == "    --":
                cmd_slave += line[2:]
        ssh.exec_command('mkdir -p $HOME/.kube')
        ssh.exec_command('sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config')
        ssh.exec_command('sudo chown $(id -u):$(id -g) $HOME/.kube/config')
        ssh.exec_command('kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml')
        time.sleep(30)
    
    # Lancement de k8s sur les slave nodes    
    for slave in CLUSTER["Slaves"]:
        ssh.connect(hostname=slave["Dns_Name"], username='ubuntu', pkey=k)
        ssh.exec_command('sudo hostnamectl set-hostname slave')
        ssh.exec_command('echo "' + slave["Ip_Address"] + '   slave" | sudo tee -a /etc/hosts')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo ' + cmd_slave + ' --ignore-preflight-errors=NumCPU')
        for line in iter(ssh_stdout.readline, ""):
            pass
        
    return 0