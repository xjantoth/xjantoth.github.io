---
title: "Verify binaries"
date: 2022-02-22T15:26:23+0100
lastmod: 2022-02-22T15:26:23+0100
draft: false
description: "Verify binaries"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['binaries']
---

One has to compare the binary version which is currently running at the Kubernetes master and later on find out the PID of kubelet process.
At the very end - simply run `sha512sum /proc/<11111>/root/bin/kubelet`. Compare it with the official kubernetes binary downloadeb by `wget ...`

```
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
