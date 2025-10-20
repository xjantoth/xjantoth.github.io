---
title: "DaemonSet"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "DaemonSet"

tags: ['daemonset']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```yaml
controlplane $ cat ds.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: elasticsearch
  namespace: kube-system
  labels:
    app: elasticsearch
spec:
  selector:
    matchLabels:
      name:  elasticsearch
  template:
    metadata:
      labels:
        name: elasticsearch
    spec:
      tolerations:
      # this toleration is to have the daemonset runnable on master nodes
      # remove it if your masters can't run pods
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: elasticsearch
        image: k8s.gcr.io/fluentd-elasticsearch:1.20
```
