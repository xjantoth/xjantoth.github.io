---
title: "Taint and tolerations"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How Kubernetes taints and tolerations work together to control pod scheduling on specific nodes."

tags: ['taint', 'tolerations']
categories: ["DevOps"]
---

# Taints are set on Nodes
# Tolerations are set on Pods


##  Taints

Taints are applied to nodes to repel pods that do not have a matching toleration. The following command taints a node so that only pods tolerating `app=blue` with effect `NoSchedule` will be scheduled on it.

```bash
kubectl taint nodes arch app=blue:NoSchedule
node/arch tainted
```
Other taint effect options:

* NoSchedule
* PreferNoSchedule
* NoExecute

##  Create a corresponding pod with tolerations
```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx-controller
  name: nginx-controller
spec:
  containers:
  - image: nginx
    name: nginx-controller
  tolerations:
  - effect: NoSchedule
    key: app
    operator: Equal
    value: blue
```

Here is another practical example. First, taint the node, then create a pod with the matching toleration so it can be scheduled on the tainted node.

```yaml
kubectl taint node node01 spray=mortein:NoSchedule
node/node01 tainted

 cat bee.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: bee
  name: bee
spec:
  containers:
  - image: nginx
    name: bee
  tolerations:
  - effect: "NoSchedule"
    key: "spray"
    value: "mortein"
    operator: "Equal"
```


##  Untaint controlplane in Katacoda

To allow regular workloads to be scheduled on the controlplane node, remove the taint by appending a `-` to the taint key.

```bash
kubectl taint node  controlplane node-role.kubernetes.io/master:NoSchedule-node/controlplane untainted
```
