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
Ce projet consiste à : automatiser le déploiement de Kubernetes sur un cluster de VM sur AWS, déployer un outil de monitoring d’application dans Kubernetes (kube-opex-analytics), déployer Hadoop Spark sur un cluster Kubernetes et exécuter l’application WordCount sur votre déploiement tout ceci en monitorant l’utilisation des ressources (CPU et mémoire).

## Cloner le projet 
### Prérequis

1. Installer docker
3. Créer un fichier <i> private_config.py </i> contenant :
  ```
  ACCESS_KEY = <Clé d'accès AWS>
  SECRET_KEY = <Clé secrète AWS>
  REGION_NAME = <Région que vous souhaitez>
  username = <Nom d'utilisateur que vous souhaitez>
  ```
### Lancement

- Pour lancer votre cluster, il vous suffit de construire et lancer le conteneur Docker :
  ```
  docker build  -t projetBigData:1 . && docker run projetBigData
  ```
- Vous verrez la progression du déploiement dans les logs du contenaire, attendez le message de fin pour faire vos tests.

### Problèmes liés à l'utilisation de Kube-opex

L'interface Kube-Opex n'est pas disponible naturellement à la suite du déploiement à cause des problèmes suivants :
- Kube-Opex est installé sur le cluster Kubernetes en tant que service, et n'est donc pas disponible nativement sur le réseau externe. Deux solutions sont alors disponibles pour résoudre ce problème :
1. Générer un autre service de type load-balancer avec une configuration de redirection de port
2. Faire la redirection directement grâce à l'utilitaire ```port-forwarding``` de Kubernetes.
Pour un soucis de temps, nous avons sélectionné la seconde option. Le souci est que la commande ```kubectl port-forwarding``` est une commande bloquante utilisée normalement à des fins de test. Elle n'est donc ni robuste ni stable, et n'est d'ailleurs pas compatible avec notre biliothèque de configuration des machines en ssh. (```paramiko```)

Pour démarrer malgré tout l'interface, il faut :
- se connecter au master-node de notre cluster en ssh avec la clé générée
```
ssh -i [username]_key.pem ubuntu@[master_dns_name]
```
- éxécuer la commande suivante :
```
kubectl port-forward service/deploy1-kube-opex-analytics 8080:80 --address 0.0.0.0
```
L'interface est alors disponible depuis n'importe quel navigateur à l'adresse [https://[master_dns_name]:8080](https://[master_dns_name]:8080)

- Cependant, un deuxième problème survient, nous n'avons pas accès aux métriques d'utilisation mémoire et CPU de notre application s'éxecutant sous kubernetes.

### Arrêt du cluster

Pour terminer les instances AWS de votre cluster, une seule commande est nécessaire :
  ```
  python3 stop.py
  ```
