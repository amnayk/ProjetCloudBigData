kubectl get events --sort-by=.metadata.creationTimestamp



# install jdk 14.0.1
sudo apt install openjdk-14-jre-headless -y

# Installer Spark sur le master :
wget http://sd-127206.dedibox.fr/hagimont/software/spark-2.4.3-bin-hadoop2.7.tgz && tar zxvf spark-2.4.3-bin-hadoop2.7.tgz


# Variables d'environnement > bashrc + sourcer

echo 'export JAVA_HOME="/usr/lib/jvm/java-14-openjdk-amd64"
export SPARK_HOME="/home/ubuntu/spark-2.4.3-bin-hadoop2.7"
export PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"' >> ~/.bashrc && source .bashrc


# copier wordcount et docker file depuis machine perso
import os, os.system("cmd")

scp -i amnay_key.pem -r wordcount ubuntu@ec2-15-237-115-165.eu-west-3.compute.amazonaws.com:~/spark-2.4.3-bin-hadoop2.7

scp -i amnay_key.pem -r Dockerfile ubuntu@ec2-15-237-115-165.eu-west-3.compute.amazonaws.com:~/spark-2.4.3-bin-hadoop2.7/kubernetes/dockerfiles/spark/Dockerfile

# [NOTUSED]changer kuberneters client

RUN rm /opt/spark/jars/kubernetes-client-4.1.2.jar
ADD https://repo1.maven.org/maven2/io/fabric8/kubernetes-client/4.4.2/kubernetes-client-4.4.2.jar /opt/spark/jars

# login

sudo docker login -u amnayk -p Amnaykdo2408

# build docker image

(Dockerfile est là : )

cd spark-2.4.3-bin-hadoop2.7/ 

sudo bin/docker-image-tool.sh -r docker.io/amnayk -t latest41 build

sudo bin/docker-image-tool.sh -r docker.io/amnayk -t latest41 push

# we need to create a service account with kubectl for Spark:

kubectl create serviceaccount spark && kubectl create clusterrolebinding spark-role --clusterrole=edit  --serviceaccount=default:spark --namespace=default

# aws cli pour tester
sudo apt install unzip -y

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# proxy

kubectl proxy&

# submit 

spark-submit \
  --deploy-mode cluster \
  --class wordCount.WordCount \
  --master k8s://https://172.31.45.171:6443\
  --conf spark.executor.instances=4 \
  --conf spark.app.name=wc \
  --conf spark.kubernetes.container.image=amnayk/spark:latest72 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  local:///opt/spark/work-dir/wc.jar


  local:///opt/spark/examples/jars/spark-examples_2.11-2.4.3.jar	
  
spark-submit \
  --deploy-mode client \
  --class wordCount.WordCount \
  --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.6 \
  --master k8s://https://172.31.29.75:6443\
  --conf spark.kubernetes.file.upload.path=s3a://sanchoss \
  --conf spark.hadoop.fs.s3a.access.key=<clef_access> \
  --conf spark.hadoop.fs.s3a.endpoint=s3.eu-west-3.amazonaws.com \
  --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
  --conf spark.hadoop.fs.s3a.fast.upload=true \
  --conf spark.hadoop.fs.s3a.secret.key=<clef_secret>  \
  --conf spark.executor.instances=3 \
  --conf spark.app.name=wc \
  --conf spark.driver.host=172.31.29.75\
  --conf spark.kubernetes.container.image=amnayk/spark:latest41 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.executor.extraJavaOptions='-Dcom.amazonaws.services.s3.enableV4' \
  /home/ubuntu/wordcount/wc.jar s3a://sanchoss/filesample.txt



spark-submit \
  --deploy-mode client \
  --class wordCount.WordCount \
  --packages com.amazonaws:aws-java-sdk:1.11.217,org.apache.hadoop:hadoop-aws:3.1.1 \
  --master k8s://https://172.31.29.75:6443\
  --conf spark.kubernetes.file.upload.path=s3a://sanchoss \
  --conf spark.hadoop.fs.s3a.access.key=<clef_access> \
  --conf spark.hadoop.fs.s3a.endpoint=s3.eu-west-3.amazonaws.com \
  --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
  --conf spark.hadoop.fs.s3a.acl.default=BucketOwnerFullControl\
  --conf spark.hadoop.fs.s3a.aws.credentials.provider=com.amazonaws.auth.InstanceProfileCredentialsProvider \
  --conf spark.hadoop.com.amazonaws.services.s3a.enableV4=true \
  --conf spark.hadoop.fs.s3a.fast.upload=true \
  --conf spark.hadoop.fs.s3a.secret.key=<clef_secret> \
  --conf spark.executor.instances=3 \
  --conf spark.app.name=wc \
  --conf spark.driver.host=172.31.29.75\
  --conf spark.kubernetes.container.image=amnayk/spark:latest41 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.executor.extraJavaOptions='-Dcom.amazonaws.services.s3.enableV4' \
  /home/ubuntu/wordcount/wc.jar s3a://sanchoss/filesample.txt



  local:///opt/spark/work-dir/wc.jar



spark-submit   
  --deploy-mode client   
  --class wordCount.WordCount   
  --master k8s://https://172.31.45.171:6443  
  --conf spark.executor.instances=2   
  --conf spark.app.name=wc   
  --conf spark.kubernetes.container.image=amnayk/spark:latest71  
  --conf spark.driver.host=master
  --conf spark.kubernetes.authenticate.driver serviceAccountName=spark   
  /home/ubuntu/wordcount/wc.jar


wordcount.py s3://inputbucket/input.txt s3://outputbucket/


  scp -i amnay_key.pem wordcount/filesample.txt ubuntu@'ec2-35-180-66-242.eu-west-3.compute.amazonaws.com:~/ww


# ce que Sam utilise de son côté
spark-submit \
  --master k8s://https://172.31.23.181:6443/ \
  --deploy-mode cluster \
  --conf spark.app.name=wc \
  --class wordCount.WordCount \
  --conf spark.executor.instances=2 \
  --conf spark.kubernetes.driver.request.cores=1 \
  --conf spark.kubernetes.executor.request.cores=1 \
  --conf spark.kubernetes.container.image=amnayk/spark:latesta99 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  local:///opt/spark/work-dir/wc.jar /opt/spark/work-dir/filesample.txt