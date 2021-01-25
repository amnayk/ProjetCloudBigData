kubectl get events --sort-by=.metadata.creationTimestamp



# install jdk 14.0.1
sudo apt install openjdk-14-jre-headless -y

# Installer Spark sur le master :
wget http://sd-127206.dedibox.fr/hagimont/software/spark-2.4.3-bin-hadoop2.7.tgz


tar zxvf spark-2.4.3-bin-hadoop2.7.tgz

# Mettre dans le bashrc du master :

echo 'export JAVA_HOME="/usr/lib/jvm/java-14-openjdk-amd64"
export SPARK_HOME="/home/ubuntu/spark-2.4.3-bin-hadoop2.7"
export PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"' >> ~/.bashrc


# Sourcer le bashrc

source .bashrc

# copier wordcount et docker file depuis machine perso
import os, os.system("cmd")

scp -i amnay_key.pem -r wordcount ubuntu@ec2-15-237-132-106.eu-west-3.compute.amazonaws.com:~/spark-2.4.3-bin-hadoop2.7

scp -i amnay_key.pem -r Dockerfile ubuntu@ec2-15-237-132-106.eu-west-3.compute.amazonaws.com:~/spark-2.4.3-bin-hadoop2.7/kubernetes/dockerfiles/spark/Dockerfile

# [NOTUSED]changer kuberneters client

RUN rm /opt/spark/jars/kubernetes-client-4.1.2.jar
ADD https://repo1.maven.org/maven2/io/fabric8/kubernetes-client/4.4.2/kubernetes-client-4.4.2.jar /opt/spark/jars

# login

sudo docker login -u amnayk -p Amnaykdo2408

# build docker image

(Dockerfile est là : )

cd spark-2.4.3-bin-hadoop2.7/ 

sudo bin/docker-image-tool.sh -r docker.io/amnayk -t latest100 build

sudo bin/docker-image-tool.sh -r docker.io/amnayk -t latest100 push

# we need to create a service account with kubectl for Spark:

kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit  --serviceaccount=default:spark --namespace=default

# proxy

kubectl proxy&

# submit 

spark-submit \
  --deploy-mode cluster \
  --class wordCount.WordCount \
  --master k8s://https://172.31.17.108:6443\
  --conf spark.executor.instances=3 \
  --conf spark.app.name=wc \
  --conf spark.kubernetes.container.image=amnayk/spark:latest100 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  local:///opt/spark/work-dir/wc.jar


  local:///opt/spark/examples/jars/spark-examples_2.11-2.4.3.jar	
  
