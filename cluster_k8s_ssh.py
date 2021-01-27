import time
import paramiko
from scp import SCPClient
from private_config import username

KEY_NAME = username+"_key"

# Config de la connection ssh permettant de se co aux masters et slaves
def open_ssh():
    k = paramiko.RSAKey.from_private_key_file(KEY_NAME + ".pem")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("ssh.log")
    return [ssh, k]

def lancer_k8s_ssh(CLUSTER):
    ssh = open_ssh()[0]
    k = open_ssh()[1]
    # Lancement des commandes d'initialisation (installation des programmes nécessaires essentiellement) sur toutes les instances (qu'elles soient master ou slave)
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

        # print("""$ echo "net.bridge.bridge-nf-call-ip6tables = 1\nnet.bridge.bridge-nf-call-iptables = 1" | sudo tee -a /etc/sysctl.d/k8s.conf""")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            'echo "net.bridge.bridge-nf-call-ip6tables = 1\nnet.bridge.bridge-nf-call-iptables = 1" | sudo tee -a /etc/sysctl.d/k8s.conf'
        )
        for line in iter(ssh_stdout.readline, ""):
            pass

        # print("$ sudo sysctl --system")
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

def lancer_spark_on_k8s_ssh(CLUSTER):
    ssh = open_ssh()[0]
    k = open_ssh()[1]
    for master in CLUSTER["Masters"]:
        ssh.connect(hostname=master["Dns_Name"], username='ubuntu', pkey=k)
        
        _, ssh_stdout, _ = ssh.exec_command('sudo apt install openjdk-14-jre-headless -y')
        for line in iter(ssh_stdout.readline, ""):
            pass
        
        _, ssh_stdout, _ = ssh.exec_command('wget http://sd-127206.dedibox.fr/hagimont/software/spark-2.4.3-bin-hadoop2.7.tgz && tar zxvf spark-2.4.3-bin-hadoop2.7.tgz')
        for line in iter(ssh_stdout.readline, ""):
            pass
        
        ssh.exec_command("echo '" + 'export JAVA_HOME="/usr/lib/jvm/java-14-openjdk-amd64"\n' +
'export SPARK_HOME="/home/ubuntu/spark-2.4.3-bin-hadoop2.7"\n' + 
'export PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"' + "' >> ~/.bashrc && source .bashrc")
        
        scp = SCPClient(ssh.get_transport())
        scp.put('wordcount', recursive=True, remote_path='~/spark-2.4.3-bin-hadoop2.7')
        scp.put('SparkDockerfile', '~/spark-2.4.3-bin-hadoop2.7/kubernetes/dockerfiles/spark/Dockerfile')
        scp.close()

        _, ssh_stdout, _ = ssh.exec_command('sudo docker login -u amnayk -p Amnaykdo2408')
        for line in iter(ssh_stdout.readline, ""):
            pass

        ssh.exec_command('cd spark-2.4.3-bin-hadoop2.7/ && sudo bin/docker-image-tool.sh -r docker.io/amnayk -t derniere build')
        time.sleep(30)

        ssh.exec_command('cd spark-2.4.3-bin-hadoop2.7/ && sudo bin/docker-image-tool.sh -r docker.io/amnayk -t derniere push')
        time.sleep(90)

        _, ssh_stdout, _ = ssh.exec_command('kubectl create serviceaccount spark && kubectl create clusterrolebinding spark-role --clusterrole=edit  --serviceaccount=default:spark --namespace=default')
        for line in iter(ssh_stdout.readline, ""):
            pass

        ssh.exec_command('kubectl proxy&')
        time.sleep(4)

        master_spark = "k8s://https://" + master["Private_Ip_Address"]+":6443"
        num_executor = len(CLUSTER["Slaves"])

        ssh.exec_command('spark-submit \
  --master ' + master_spark + ' \
  --deploy-mode cluster \
  --conf spark.app.name=wc \
  --class wordCount.WordCount \
  --conf spark.executor.instances='+ str(num_executor) + ' \
  --conf spark.kubernetes.driver.request.cores=1 \
  --conf spark.kubernetes.executor.request.cores=1 \
  --conf spark.kubernetes.container.image=amnayk/spark:derniere \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  local:///opt/spark/work-dir/wc.jar')
