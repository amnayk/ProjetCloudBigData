# install jdk 14.0.1
sudo apt install openjdk-14-jre-headless 

# Installer Spark sur le master :
wget http://sd-127206.dedibox.fr/hagimont/software/spark-2.4.3-bin-hadoop2.7.tgz
tar zxvf spark-2.4.3-bin-hadoop2.7.tgz

# Mettre dans le bashrc du master :
export JAVA_HOME="/usr/lib/jvm/java-14-openjdk-amd64"
export SPARK_HOME="/home/ubuntu/spark-2.4.3-bin-hadoop2.7"
export PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"

# Sourcer le bashrc

source .bashrc

# copier wordcount

scp -i amnay_key.pem -r wordcount/ ubuntu@ec2-35-180-73-9.eu-west-3.compute.amazonaws.com:~/spark-2.4.3-bin-hadoop2.7/

# login

docker login

# build docker image

(Dockerfile est là : )

cd spark-2.4.3-bin-hadoop2.7/ 

sudo bin/docker-image-tool.sh -r docker.io/amnayk -t latest build

sudo bin/docker-image-tool.sh -r docker.io/amnayk -t latest push

# we need to create a service account with kubectl for Spark:

kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit  --serviceaccount=default:spark --namespace=default

# proxy

kubectl proxy&

# submit 

spark-submit \
  --deploy-mode cluster \
  --class home.sam.eclipse-wspace.ProjetBigSanchos.wordCount.WordCount \
  --master k8s://https://172.31.17.72:6443\
  --conf spark.executor.instances=3 \
  --conf spark.app.name=wc \
  --conf spark.kubernetes.container.image=amnayk/spark \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  local:///opt/spark/wordcount/wc.jar


  local:///opt/spark/examples/jars/spark-examples_2.11-2.4.3.jar	
  
  





  --conf spark.kubernetes.driver.docker.image=kubespark/spark-driver:v2.2.0-kubernetes-0.5.0 \
  --conf spark.kubernetes.executor.docker.image=kubespark/spark-executor:v2.2.0-kubernetes-0.5.0 \






  ------------------------------------------


# Amnay

bin/spark-submit --master k8s://https://172.31.19.69:6443 --deploy-mode cluster
--name wordcount --conf spark.executor.instances=2
--conf spark.kubernetes.driver.container.image=spark/spark-py  --py-files http://0.0.0.0:30001/wordcount.py


spark-submit \
    --master k8s://https://172.31.17.165:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=3 \
    --conf spark.kubernetes.container.image=spark:latest \
    local:///opt/spark/examples/jars/spark-examples_2.11-2.4.3.jar




spark-submit --master k8s://https://172.31.20.122:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=3 \
    --executor-memory 1024m \
    --conf spark.kubernetes.container.image=spark:latest \
    local:///home/ubuntu/spark-2.4.3-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.4.3.jar

# last one 

spark-submit \
    --master k8s://https://172.31.19.69:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=spark/spark \
    local:///opt/spark/examples/jars/spark-examples_2.11-2.4.3.jar





    SparkSession spark = SparkSession
                .Builder()
                .Config("spark.driver.host","127.0.0.1")
                .AppName("word_count_sample")
                .GetOrCreate();


# AMNAY LE BOSS

# install jdk 14.0.1
sudo apt install openjdk-14-jre-headless 

# Installer Spark sur le master :
wget http://sd-127206.dedibox.fr/hagimont/software/spark-2.4.3-bin-hadoop2.7.tgz
tar zxvf spark-2.4.3-bin-hadoop2.7.tgz

# Mettre dans le bashrc du master :
export JAVA_HOME="/usr/lib/jvm/java-14-openjdk-amd64"
export SPARK_HOME="/home/ubuntu/spark-2.4.3-bin-hadoop2.7"
export PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"



# build docker image

cd spark-2.4.3-bin-hadoop2.7/ 
sudo bin/docker-image-tool.sh -r spark -t latest build

# we need to create a service account with kubectl for Spark:

kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit  --serviceaccount=default:spark --namespace=default

# spark submit

spark-submit \
    --master k8s://https://172.31.21.202:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=spark \
    --conf spark.kubernetes.container.image.pullPolicy=Never \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    local:///opt/spark/examples/jars/spark-examples_2.11-2.4.3.jar

spark-submit \
    --master k8s://https://172.31.21.202:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=spark:latest \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    local:///opt/spark/examples/jars/spark-examples_2.11-2.4.3.jar


sudo docker login

sudo docker pull bitnami/spark:latest

spark-submit \
    --master k8s://https://172.31.21.202:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=bitnami/spark \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    local:///opt/spark/examples/jars/spark-examples_2.11-2.4.3.jar




spark-submit \
  --deploy-mode cluster \
  --class org.apache.spark.examples.SparkPi \
  --master k8s://https://172.31.21.202:6443 \
  --conf spark.executor.instances=2 \
  --conf spark.app.name=spark-pi \
  --conf spark.kubernetes.container.image=amnayk/spark \
  --conf spark.kubernetes.driver.docker.image=kubespark/spark-driver:v2.2.0-kubernetes-0.5.0 \
  --conf spark.kubernetes.executor.docker.image=kubespark/spark-executor:v2.2.0-kubernetes-0.5.0 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  local:///opt/spark/examples/jars/spark-examples_2.11-2.4.3.jar


