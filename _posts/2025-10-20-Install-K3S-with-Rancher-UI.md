---
title: "Install K3S with Rancher UI"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "Install K3S with Rancher UI"

tags: ["kubernetes", "install", "rancher", "ui", "k3s"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##  Adjust your /etc/hosts file

```
# Adjust your /etc/hosts file
cat /etc/hosts
...
192.168.1.45    archlinux
...
:wq!
```

##  Deploy K3S cluster yo tour local
##
```
# Deploy K3S cluster yo tour local
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--datastore-endpoint etcd --no-deploy traefik" sh -s -

sudo chmod  755 /etc/rancher/k3s/k3s.yaml
kubectl get pods -A
```

##  Deploy Nginx Ingress Controller

```
# Deploy Nginx Ingress Controller
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update

helm install nginx stable/nginx-ingress  \
--set controller.service.type=NodePort \
--set controller.service.nodePorts.https=30111
```

##  Rancher with certificates generation

```
mkdir -p /home/jantoth/etc/pki/tls/private
mkdir -p /home/jantoth/etc/pki/tls/certs

NAME="archlinux"
RANCHER_URL="https://$NAME:30111"
PRIVATE="/home/jantoth/etc/pki/tls/private"   # *.key
CERTS="/home/jantoth/etc/pki/tls/certs"       # *.crt

if [ ! -f "${PRIVATE}/${NAME}.key" ]; then

    echo "INFO: generating CA for Rancher"
    openssl genrsa -out "${PRIVATE}/${NAME}-ca.key" 4096

    openssl req -key "${PRIVATE}/${NAME}-ca.key" \
    -subj "/C=EU/ST=SD/L=AM/O=${NAME}/CN=Authority" \
    -new -x509 -days 7300 -sha256 \
    -out "${CERTS}/${NAME}-ca.crt" -extensions v3_ca

    echo "INFO: generating private key and certificate for Rancher"
    openssl genrsa -out "${PRIVATE}/${NAME}.key" 4096

    openssl req -key "${PRIVATE}/${NAME}.key" \
    -new -sha256 -out "${CERTS}/${NAME}.csr" \
     -subj "/C=EU/ST=SD/L=AM/O=${NAME}/CN=${NAME}"

    openssl x509 -req -CA "${CERTS}/${NAME}-ca.crt" -CAkey "${PRIVATE}/${NAME}-ca.key" \
    -CAcreateserial -in "${CERTS}/${NAME}.csr" \
    -out "${CERTS}/${NAME}.crt" -days 7300

    cp "${CERTS}/${NAME}-ca.crt" "${CERTS}/cacerts.pem"

fi

kubectl create namespace cattle-system

kubectl -n cattle-system get secret tls-rancher-ingress &>/dev/null ||
    kubectl -n cattle-system create secret tls tls-rancher-ingress \
        --cert="${CERTS}/${NAME}.crt" --key="${PRIVATE}/${NAME}.key"

kubectl -n cattle-system get secret tls-ca &>/dev/null ||
    kubectl -n cattle-system create secret generic tls-ca \
        --from-file="${CERTS}/cacerts.pem"
```
##  Deploy Rancher to K3S/K8S

```
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
helm repo update

kubectl create namespace cattle-system
helm install \
rancher rancher-stable/rancher \
--namespace cattle-system \
--set hostname=archlinux \
--set replicas=1 \
--set tls=ingress  \
--set ingress.tls.source=secret \
--set privateCA=true
```

##  Longhorn setup

```
sudo pacman -S community/open-iscsi
sudo systemctl enable --now iscsid
```



##  Using cert-manager to provide SSL certificates for Rancher (overkill)

```

# Install the CustomResourceDefinition resources separately
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.15.0/cert-manager.crds.yaml

kubectl create namespace cert-manager

helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
helm repo update

# Install the cert-manager Helm chart
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --version v0.15.0

kubectl get pods --namespace cert-manager


helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
helm repo update

kubectl create namespace cattle-system


helm install \
rancher rancher-stable/rancher \
--namespace cattle-system \
--set hostname=archlinux \
--set replicas=1

# Setup Coredns pod

# kubectl rollout restart -n kube-system deployment/coredns

```

##  Login to Rancher via rancher cli

```
NAME="archlinux"
RANCHER_URL="https://$NAME:30111"

APITOKEN=$(curl -sk "${RANCHER_URL}/v3-public/localProviders/local?action=login" \
-H "content-type: application/json" \
--data-binary "{\"username\":\"admin\",\"password\":\"admin\"}" 2>/dev/null | jq -r .token 2>/dev/null)

rancher login -t "${APITOKEN}" "${RANCHER_URL}/v3"
```
