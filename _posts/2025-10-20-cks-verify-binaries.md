---
title: "Verify binaries"
date: 2022-02-22T15:26:23+0100
lastmod: 2022-02-22T15:26:23+0100
draft: false
description: "How to verify the integrity of Kubernetes binaries by comparing SHA-512 checksums of running processes against officially released binaries."
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['binaries']
categories: ["DevOps"]
---

One has to compare the binary version which is currently running at the Kubernetes master and later on find out the PID of kubelet process.
At the very end, simply run `sha512sum /proc/<PID>/root/bin/kubelet`. Compare it with the official Kubernetes binary downloaded by `wget`.

The following commands download the official Kubernetes server binaries, compute the SHA-512 hash of the kubelet binary, find the PID of the running kubelet process, and compare the hashes to verify integrity.

```bash
kubectl get pods
kubectl get nodes
wget https://dl.k8s.io/v1.23.1/kubernetes-server-linux-amd64.tar.gz
tar -xvzf *.tar.gz

sha512sum kubernetes/server/bin/kubelet | cut -d" " -f1 > compare
ps -ef | grep kubelet
sha512sum /proc/23213/root/bin/kubelet | cut -d" " -f 1 >> compare
cat compare  | uniq
echo DIFFERENT > /answer
```
