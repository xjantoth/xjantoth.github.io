---
title: "How to get PID of the main process in containers to be used for strace"
date: 2025-12-21T21:49:54:+0100
lastmod: 2025-12-21T21:49:54:+0100
draft: false
description: "How to get PID of the main process in containers to be used for strace"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ["cks", "strace", "kubernetes", "awk", "crictl", "custom-columns"]
---

Hwo to get PID of the main process in a container used later on to check strace. Needed for CKS Kubernetes certification.


```bash
controlplane:~$ kubectl get pod -n kube-system  -o custom-columns="ID :.status.containerStatuses[0].containerID,P:.metadata.name,N:.spec.nodeName" --no-headers | \ 
awk '{print "ssh "$3 " -- sudo crictl inspect " substr($1,14,14) " | \
yq '.info.pid' # " $2}'

ssh controlplane -- sudo crictl inspect 5f8c726880ff84 | yq .info.pid # calico-kube-controllers-7bb4b4d4d-6w29j
ssh controlplane -- sudo crictl inspect ee8a4b8c58b1fc | yq .info.pid # canal-27xx6
ssh node01 -- sudo crictl inspect 1274fb54799d9e | yq .info.pid # canal-qq47f
ssh node01 -- sudo crictl inspect b88cd53b37d8dd | yq .info.pid # coredns-76bb9b6fb5-lqht4
ssh node01 -- sudo crictl inspect 18a6c9051aa852 | yq .info.pid # coredns-76bb9b6fb5-n9cf6
ssh controlplane -- sudo crictl inspect 9f5178c2003500 | yq .info.pid # etcd-controlplane
ssh controlplane -- sudo crictl inspect 0da74ddfd9038c | yq .info.pid # kube-apiserver-controlplane
ssh controlplane -- sudo crictl inspect a1110c9f2e073b | yq .info.pid # kube-controller-manager-controlplane
ssh node01 -- sudo crictl inspect 24b8ed406a6d46 | yq .info.pid # kube-proxy-x9wth
ssh controlplane -- sudo crictl inspect a2e225b55b6b07 | yq .info.pid # kube-proxy-zdx2k
ssh controlplane -- sudo crictl inspect e0c125f4059102 | yq .info.pid # kube-scheduler-controlplane
```
