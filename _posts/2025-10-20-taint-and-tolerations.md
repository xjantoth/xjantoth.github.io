---
title: "taint and tolerations"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "taint and tolerations"

tags: ['taint', 'tolerations']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

# taints are set to ''Nodes''
# toleration are set to ''PODS''


##  taints:
```
kubectl taint nodes arch app=blue:NoSchedule
node/arch tainted
```
Other ''taint'' options:

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

practice

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


##  untaint controlplane in katacoda

```
kubectl taint node  controlplane node-role.kubernetes.io/master:NoSchedule-node/controlplane untainted
```
