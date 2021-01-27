import paramiko
from scp import SCPClient
import sys
import time


def launch(vm, KEY_NAME):
    k = paramiko.RSAKey.from_private_key_file(KEY_NAME + ".pem")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("ssh.log")

    print("Installing kubeopex on "+str(vm['Id_Instance']))
    ssh.connect(hostname=vm["Dns_Name"], username='ubuntu', pkey=k)

    # Define progress callback that prints the current percentage completed for the file
    def progress(filename, size, sent):
        sys.stdout.write("%s's progress: %.2f%%   \r" %
                         (filename, float(sent)/float(size)*100))

    # SCPCLient takes a paramiko transport as an argument
    transport = ssh.get_transport()
    scp = SCPClient(transport, progress=progress)

    # Intalling Helm
    print("    ###### Intalling Helm ######")
    print("    $ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        'curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3')
    for line in iter(ssh_stdout.readline, ""):
        print(line)

    print("    $ chmod 700 get_helm.sh")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        'chmod 700 get_helm.sh')
    for line in iter(ssh_stdout.readline, ""):
        print(line)

    print("    $ ./get_helm.sh")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        './get_helm.sh')
    for line in iter(ssh_stdout.readline, ""):
        print(line)

    # Cloning Kube-opex
    print("    ###### Cloning Kube-opex ######")
    print("    $ git clone https://github.com/rchakode/kube-opex-analytics")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        'git clone https://github.com/rchakode/kube-opex-analytics')
    for line in iter(ssh_stdout.readline, ""):
        print(line)

    # Kubectl Metrics Server
    print("    ###### Kubectl Metrics Server ######")
    print("    $ kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        'kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml')
    for line in iter(ssh_stdout.readline, ""):
        print(line)

    # Create PersistentVolume
    print("    ###### Create PersistentVolume ######")
    print("    $ git clone https://github.com/rchakode/kube-opex-analytics")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        'git clone https://github.com/rchakode/kube-opex-analytics')
    for line in iter(ssh_stdout.readline, ""):
        print(line)

    print("    $ scp -i "+KEY_NAME+".pem -r pv.yaml ubuntu@" +
          vm["Dns_Name"]+":~/pv.yaml")
    scp.put('pv.yaml', '~/pv.yaml')

    print("    $ kubectl apply -f ~/pv.yaml")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        'kubectl apply -f ~/pv.yaml')
    for line in iter(ssh_stdout.readline, ""):
        print(line)

    # Intall KubeOpex
    print("    ###### Intall KubeOpex ######")
    print("    TODO : $ nano kube-opex-analytics/helm/kube-opex-analytics/values.yaml")
    print("    $ helm install deploy1 kube-opex-analytics/helm/kube-opex-analytics/")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        'helm install deploy1 kube-opex-analytics/helm/kube-opex-analytics/')
    for line in iter(ssh_stdout.readline, ""):
        print(line)

    time.sleep(10)

    # print("    $ kubectl port-forward service/deploy1-kube-opex-analytics 8080:80 --address 0.0.0.0")
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
    #     'kubectl port-forward service/deploy1-kube-opex-analytics 8080:80 --address 0.0.0.0')
    # for line in iter(ssh_stdout.readline, ""):
    #     print(line)
