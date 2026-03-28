---
title: "CKS run kubernetes with cri-o"
date: 2022-06-28T13:33:39+0200
lastmod: 2022-06-28T13:33:39+0200
draft: false
description: "How to install and run Kubernetes with CRI-O as the container runtime, including crictl configuration, kubeadm initialization, and building images with buildah."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'kubernetes']
categories: ["Kubernetes"]
---


## How to run Kubernetes with CRI-O

The following commands install CRI-O as the container runtime on Ubuntu. This involves adding the CRI-O package repositories, importing their GPG keys, and then installing the CRI-O packages along with the `cri-tools` utility.

```bash
# Reference: https://computingforgeeks.com/install-cri-o-container-runtime-on-ubuntu-linux/

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

Configure `crictl` to communicate with the CRI-O runtime by specifying the correct socket endpoint in `/etc/crictl.yaml`.

```yaml
cat /etc/crictl.yaml
runtime-endpoint: "unix:///var/run/crio/crio.sock"
timeout: 0
debug: false
# runtime-endpoint: unix:///run/containerd/containerd.sock
```

Initialize a Kubernetes cluster using `kubeadm` with either CRI-O or Containerd as the container runtime. The `--cri-socket` flag specifies which runtime socket to use.

```bash
# Run Kubernetes with CRI-O
kubeadm init --kubernetes-version=${KUBE_VERSION} --ignore-preflight-errors=NumCPU,Mem --skip-token-print --pod-network-cidr 192.168.0.0/16 --cri-socket unix:///var/run/crio/crio.sock

# Run Kubernetes with Containerd
kubeadm init --kubernetes-version=${KUBE_VERSION} --ignore-preflight-errors=NumCPU,Mem --skip-token-print --pod-network-cidr 192.168.0.0/16 --cri-socket unix:///run/containerd/containerd.sock

```


##### Simple Dockerfile

This minimal Dockerfile creates an nginx-based image with a custom index page. It can be built locally with `buildah` and run directly on a CRI-O-powered cluster.

```dockerfile
cat Dockerfile
FROM nginx:alpine
RUN echo "Buildha dude!" > /usr/share/nginx/html/index.html
```

##### Run locally built container via `buildah`

The following commands build a container image locally using `buildah`, list available images via `crictl`, and then deploy the image as a pod in the cluster. The service is edited to use a NodePort for external access.

```bash
k taint node scw-k8s-cmdx node-role.kubernetes.io/master-
buildah -t mk:jt bud -f Dockerfile
crictl images
k run mk --image=localhost/mk:jt --expose --port 80
k get pods,svc
k edit svc mk
curl localhost:30888
```
