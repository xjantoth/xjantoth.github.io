---
title: "CKS run kubernetes with cri-o"
date: 2022-06-28T13:33:39+0200
lastmod: 2022-06-28T13:33:39+0200
draft: false
description: "CKS run kubernetes with cri-o"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'kubernetes']
---


## How to run Kubernetes with cri-o

```
https://computingforgeeks.com/install-cri-o-container-runtime-on-ubuntu-linux/

OS=xUbuntu_20.04
CRIO_VERSION=1.23
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /"|sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
echo "deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$CRIO_VERSION/$OS/ /"|sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$CRIO_VERSION.list

curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$CRIO_VERSION/$OS/Release.key | sudo apt-key add -
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo apt-key add -

apt update
apt install cri-o cri-o-runc

sudo systemctl enable crio.service
sudo systemctl start crio.service

apt install cri-tools
```


##### Setup crictl binary

```
cat /etc/crictl.yaml
runtime-endpoint: "unix:///var/run/crio/crio.sock"
timeout: 0
debug: false
# runtime-endpoint: unix:///run/containerd/containerd.sock
```


```
# Run Kubernetes with CRI-O
kubeadm init --kubernetes-version=${KUBE_VERSION} --ignore-preflight-errors=NumCPU,Mem --skip-token-print --pod-network-cidr 192.168.0.0/16 --cri-socket unix:///var/run/crio/crio.sock

# Run Kubernetes with Containerd
kubeadm init --kubernetes-version=${KUBE_VERSION} --ignore-preflight-errors=NumCPU,Mem --skip-token-print --pod-network-cidr 192.168.0.0/16 --cri-socket unix:///run/containerd/containerd.sock

```


##### Simple Dockerfile

```
cat Dockerfile
FROM nginx:alpine
RUN echo "Buildha dude!" > /usr/share/nginx/html/index.html
```

##### Run locally built container via `buildha`

```
k taint node scw-k8s-cmdx node-role.kubernetes.io/master-
buildah -t mk:jt bud -f Dockerfile
crictl images
k run mk --image=localhost/mk:jt --expose --port 80
k get pods,svc
k edit svc mk
curl localhost:30888
```
