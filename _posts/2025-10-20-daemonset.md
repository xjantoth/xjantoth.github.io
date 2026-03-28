---
title: "DaemonSet"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Kubernetes DaemonSet example that deploys an Elasticsearch (Fluentd) pod on every node, including master nodes."

tags: ['daemonset']
categories: ["DevOps"]
---

This DaemonSet manifest deploys an Elasticsearch (Fluentd) logging agent on every node in the cluster, including master nodes. The toleration for `node-role.kubernetes.io/master` with `NoSchedule` effect ensures the pod can run on control-plane nodes as well.

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
