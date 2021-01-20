### Todo

- [ ] Put a username tag on instances to give exclusivity to each user on its instances (So that we can stop only our instances)
- [ ] Use Kube-opex-analytics
- [ ] Report 

### In Progress

- [ ] stop.py : bug de security group
- [**] Deploy Hadoop & Spark & Run WordCount

### Done ✓

- [x] Generate key pairs for ssh connection to VMs
- [x] Create security groups
- [x] Deploy instances
  - [x] Dictionnary for the cluster's architecture
- [x] Deploy Kubernetes
 

[**] : 
ESSAYER CE QUE CHANCH A ENVOYE SUR CONV MESSENGER POUR ENLEVER LE REQUIREMENT DE 2 CPUS ! 
OU USE T2.MEDIUM ET DONC PAYER MAIS SUPPR COMPTE APRES LA FIN DU MOIS QUAND IL ME DIRA QUE PEUT PAS RETIRER LES THUNES SUR MON COMPTE !

jar cf wc.jar ~/eclipse-wspace/ProjetBigSanchos/wordCount

##

# Installer java jdk 8 sur le master :
sudo apt install openjdk-8-jre-headless

# Installer Spark sur le master :
wget http://sd-127206.dedibox.fr/hagimont/software/spark-2.4.3-bin-hadoop2.7.tgz
tar zxvf spark-2.4.3-bin-hadoop2.7.tgz

# Mettre dans le bashrc du master :
export JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk-amd64"
export SPARK_HOME="/home/ubuntu/spark-2.4.3-bin-hadoop2.7"
export PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"

# Rendre effectif les export de variables d'enviro sur le master tjrs :
source .bashrc

# build docker image

cd spark-2.4.3-bin-hadoop2.7/ 
sudo bin/docker-image-tool.sh -r spark -t latest build


# Passer en ssh depuis ma machine le wc.jar :
scp -i sam_key.pem wc.jar ubuntu@<NOMDNSDUMASTER>:.

# Lancer Spark Submit :
mettre en route le proxy sur le master : kubectl proxy


# ouvrir un autre term et :
spark-submit     --master k8s://https://<AdresseMaster(kubectl cluster-info) OU localhost>:6443     --deploy-mode cluster     --name spark-pi     --class org.apache.spark.examples.SparkPi     --conf spark.executor.instances=1     --conf spark.kubernetes.container.image=vitamingaugau/spark:spark-2.4.4     wc.jar


ouvrir un autre term pour monitorer et voir les logs de notre lancement :
kubectl get events --sort-by=.metadata.creationTimestamp