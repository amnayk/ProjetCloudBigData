<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/cchanche/esp32iot">
    <img src="images/enseeiht.jpeg" alt="Logo" width="120" height="120">
  </a>

  <h3 align="center">Projet Infrastuctures pour le Cloud et le Big Data 3A IBDIoT</h3>
  <h4 align="center"><i>CHANCHEVRIER KANANE BOURY EGRETEAU</i></h4>
</p>

## Résumé

Dans le cadre du cours sur les Infrastructures pour le Cloud et le Big Data, le projet a pour but d’approfondir les sujets abordés durant les séances de travaux pratiques.
Ce projet consiste à : automatiser le déploiement de Kubernetes sur un cluster de VM sur AWS, déployer un outil de monitoring d’application dans Kubernetes (kube-opex-analytics), déployer Hadoop Spark sur votre cluster Kubernetes et exécuter l’application WordCount sur votre déploiement tout ceci en monitorant l’utilisation des ressources (CPU et mémoire).

## Cloner le projet 
### Prérequis

1. Installer python3
2. Installer le package boto3 grâce à pip
3. Créer un fichier <i> private_config.py </i> contenant :
  ```py
  ACCESS_KEY = <Clé d'accès AWS>
  SECRET_KEY = <Clé secrète AWS>
  REGION_NAME = <Région que vous souhaitez>
  username = <Nom d'utilisateur que vous souhaitez>
  ```
### Lancement

- Pour lancer votre cluster, il vous suffit d'une commande :
  ```
  python3 deploy.py -u <Nom d'utilisateur choisi avant> -m <Nombre de master(s)> -w <Nombre de worker(s)>
  ```
- Le lancement finit sur un wait() bloquant, cependant, cela ne gêne pas le lancement de notre cluster, le lancement des pods spark dans kubernetes et la bonne exécution de notre application wordcount à l'intérieur de ceux-ci.

### Problèmes liés à l'utilisation de Kube-opex

- Concernant l'application de monitoring Kube-opex, nous n'avons pas réussi à incorporer dans notre fichier python d'automatisation le lancement de la commande de port-forwarding en ssh car c'est une commande bloquante. Il vous suffit donc de vous connecter en ssh au master en utilisant son adresse DNS publique et ensuite de taper dans son terminal :
  ```
  TODOBEM
  ```
- Cependant, un deuxième problème survient, nous n'avons pas accès aux métriques d'utilisation mémoire et CPU de notre application s'éxecutant sous kubernetes.

### Arrêt du cluster

Pour terminer les instances AWS de votre cluster, une seule commande est nécessaire :
  ```
  python3 stop.py
  ```
