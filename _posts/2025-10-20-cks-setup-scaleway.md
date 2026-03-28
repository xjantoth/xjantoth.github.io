---
title: "CKS setup Scaleway kubernetes cluster at Ubuntu 18.04"
date: 2022-01-14T14:30:55+01:00
lastmod: 2022-01-14T14:31:00+01:00
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Step-by-step guide to setting up a Kubernetes cluster on Scaleway with Ubuntu, including SSH key generation, instance creation, and kubeadm initialization."

tags: ['cks', 'setup', 'scaleway', 'kubernetes', 'cluster', 'ubuntu']
categories: ["Kubernetes"]
---


Create an SSH key pair to be used for authenticating to the Kubernetes master and node machines on Scaleway.

```bash
ssh-keygen -f ~/.ssh/scw-k8s-cks -t rsa -b 4096 -C "toth.janci@gmail.com"
```

If you want to create a new instance via the command-line **scw** binary, the following command provisions a DEV1-S instance running Ubuntu Focal with a 20GB root volume.

```bash
scw instance server create type=DEV1-S zone=fr-par-1 image=ubuntu_focal root-volume=l:20G name=scw-k8s-cks ip=new project-id=431d432b-1849-445f-a66b-7d1ccdf5d34a
```

SSH to the machine using the previously generated key pair.

```bash
ssh -i ~/.ssh/scw-k8s-cks  root@51.158.106.182
```

Provision the Kubernetes master node using the CKS course setup script. This script handles installing kubeadm, kubelet, kubectl, and initializing the control plane.

```bash
bash <(curl -s https://raw.githubusercontent.com/killer-sh/cks-course-environment/master/cluster-setup/latest/install_master.sh)
```


Start the Kubernetes cluster manually if Scaleway changes your private IPv4 address after reboot. This script resets kubeadm, kills any processes occupying the required ports, re-initializes the cluster, and installs the Weave network plugin.

```bash
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
