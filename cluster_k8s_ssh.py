import paramiko


def lancer_k8s_ssh(CLUSTER, KEY_NAME):
    k = paramiko.RSAKey.from_private_key_file(KEY_NAME + ".pem")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("ssh.log")

    for vm in CLUSTER["Masters"] + CLUSTER["Slaves"]:
        print("Installing "+str(vm['Id_Instance']))
        ssh.connect(hostname=vm["Dns_Name"], username='ubuntu', pkey=k)

        print("    apt-get update...")
        # print("$ sudo apt-get update -y")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            'sudo apt-get update -y')
        for line in iter(ssh_stdout.readline, ""):
            pass

        # print("$ swapoff -a")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('swapoff -a')
        for line in iter(ssh_stdout.readline, ""):
            pass

        print("    fetching Docker...")
        # print("$ sudo wget -qO- https://get.docker.com/ | sh")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            'sudo wget -qO- https://get.docker.com/ | sh')
        for line in iter(ssh_stdout.readline, ""):
            pass

        # print("$ sudo modprobe br_netfilter")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo modprobe br_netfilter')
        for line in iter(ssh_stdout.readline, ""):
            pass

        print("""$ echo "net.bridge.bridge-nf-call-ip6tables = 1\nnet.bridge.bridge-nf-call-iptables = 1" | sudo tee -a /etc/sysctl.d/k8s.conf""")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            'echo "net.bridge.bridge-nf-call-ip6tables = 1\nnet.bridge.bridge-nf-call-iptables = 1" | sudo tee -a /etc/sysctl.d/k8s.conf'
        )
        for line in iter(ssh_stdout.readline, ""):
            pass

        print("sudo sysctl --system")
        _, ssh_stdout, _ = ssh.exec_command("sudo sysctl --system")
        for line in iter(ssh_stdout.readline, ""):
            pass

        print("    fetching Kubernetes...")
        # print("$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -")
        _, ssh_stdout, _ = ssh.exec_command(
            "curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -"
        )
        for line in iter(ssh_stdout.readline, ""):
            pass
        
        # print("$ apt-add-repo")
        _, ssh_stdout, _ = ssh.exec_command(
            'sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"'
        )
        for line in iter(ssh_stdout.readline, ""):
            pass

        # print("$ apt-get update")
        _, ssh_stdout, _ = ssh.exec_command("sudo apt-get update")
        for line in iter(ssh_stdout.readline, ""):
            pass
        
        # print("$ yes | sudo apt-get install kubelet kubeadm kubectl")
        _, ssh_stdout, _ = ssh.exec_command(
            "yes | sudo apt-get install kubelet kubeadm kubectl"
        )
        for line in iter(ssh_stdout.readline, ""):
            pass
        
        for master in CLUSTER["Masters"]:
            ssh.exec_command(
                'echo "' + master["Ip_Address"] + '   master" | sudo tee -a /etc/hosts'
            )
        for slave in CLUSTER["Slaves"]:
            ssh.exec_command(
                'echo "'
                + slave["Ip_Address"]
                + "  "
                + slave["Id_Slave"]
                + '" | sudo tee -a /etc/hosts'
            )

    cmd_slave = ""

    # Lancement de k8s sur les master nodes
    for master in CLUSTER["Masters"]:
        print("Launching Kubernetes on master "+str(master['Id_Instance']))
        ssh.connect(hostname=master["Dns_Name"], username='ubuntu', pkey=k)
        ssh.exec_command('sudo hostnamectl set-hostname master')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            'sudo kubeadm init --ignore-preflight-errors=NumCPU,Mem --pod-network-cidr=10.244.0.0/16')
        for line in iter(ssh_stdout.readline, ""):
            if line[0:7] == "kubeadm":
                cmd_slave = line[0 : len(line) - 2]
            if line[0:6] == "    --":
                cmd_slave += line[2:]
        ssh.exec_command("mkdir -p $HOME/.kube")
        ssh.exec_command("sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
        ssh.exec_command("sudo chown $(id -u):$(id -g) $HOME/.kube/config")
        _, ssh_stdout, _ = ssh.exec_command(
            "kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml"
        )
        for line in iter(ssh_stdout.readline, ""):
            pass

    # Lancement de k8s sur les slave nodes
    for slave in CLUSTER["Slaves"]:
        print("Launching Kubernetes on slave "+str(slave['Id_Instance']))
        ssh.connect(hostname=slave["Dns_Name"], username='ubuntu', pkey=k)
        ssh.exec_command('sudo hostnamectl set-hostname ' + slave["Id_Slave"])
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            'sudo ' + cmd_slave + ' --ignore-preflight-errors=NumCPU,Mem')
        for line in iter(ssh_stdout.readline, ""):
            pass

    return 0
