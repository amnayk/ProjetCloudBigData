# kube

kubectl get nodes

kubectl get events

kubectl get pods

kubectl describe storageclasses

kubectl get services

kubectl get events --sort-by=.metadata.creationTimestamp

# install helm

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3

chmod 700 get_helm.sh

./get_helm.sh

# kube-opex

git clone https://github.com/rchakode/kube-opex-analytics

# Latest Metrics Server release can be installed by running:

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Create PersistentVolume

nano pv.yaml

kubectl apply -f pv.yaml

# install kube

nano kube-opex-analytics/helm/kube-opex-analytics/values.yaml

helm install deploy1 kube-opex-analytics/helm/kube-opex-analytics/

kubectl port-forward service/deploy1-kube-opex-analytics 8080:80 --address 0.0.0.0
