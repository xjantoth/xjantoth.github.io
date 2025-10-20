---
title: "CKS setup Scaleway kubernetes cluster at Ubuntu 18.04"
date: 2022-01-14T14:30:55+01:00
lastmod: 2022-01-14T14:31:00+01:00
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "CKS setup Scaleway kubernetes cluster at Ubuntu 18.04"

tags: ['cks', 'setup', 'scaleway', 'kubernetes', 'cluster', 'at', 'ubuntu']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---


Create SSH key pair to be used for Kubernetes master and node machine

```
ssh-keygen -f ~/.ssh/scw-k8s-cks -t rsa -b 4096 -C "toth.janci@gmail.com"
```

If you want to create a new instance via command line **scw** binary

```
scw instance server create type=DEV1-S zone=fr-par-1 image=ubuntu_focal root-volume=l:20G name=scw-k8s-cks ip=new project-id=431d432b-1849-445f-a66b-7d1ccdf5d34a
```

SSH to the machine

```
ssh -i ~/.ssh/scw-k8s-cks  root@51.158.106.182
```

Provision Kubernetes master node

```
bash <(curl -s https://raw.githubusercontent.com/killer-sh/cks-course-environment/master/cluster-setup/latest/install_master.sh)
```


Start kubenretes cluste manually if Scaleway changes your private IPv4 address after reboot

```
KUBE_VERSION=1.22.2
kubeadm reset -f

for i in 10257 10259; do
    PORTD=$(netstat -tunlp | grep $i | awk {'print $7'})
    kill ${PORTD%/*}
done

kubeadm init --kubernetes-version=${KUBE_VERSION} --ignore-preflight-errors=NumCPU --skip-token-print --apiserver-cert-extra-sans="51.158.106.182"
mkdir -p ~/.kube
sudo cp /etc/kubernetes/admin.conf ~/.kube/config



# workaround because https://github.com/weaveworks/weave/issues/3927
# kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
curl -L https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n') -o weave.yaml
sed -i 's/ghcr.io\/weaveworks\/launcher/docker.io\/weaveworks/g' weave.yaml
kubectl -f weave.yaml apply
rm weave.yaml

echo
echo "### COMMAND TO ADD A WORKER NODE ###"
kubeadm token create --print-join-command --ttl 0
```
