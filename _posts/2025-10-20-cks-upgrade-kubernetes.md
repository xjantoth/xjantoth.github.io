---
title: "CKS upgrade kubernetes"
date: 2022-04-26T10:53:27+0200
lastmod: 2022-04-26T10:53:27+0200
draft: false
description: "Upgrade Master Node procedure."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'upgrade', 'kubernetes']
categories: ["Kubernetes"]
---

```
major    minor    patch
 1    .   24    .   0
```

![Image](/assets/images/blog/release.png)

##### Upgrade Master Node procedure

* drain and cordon (make it unschedulable) node
* kubeadm
* kube-apiserver
* controller-manager
* scheduler

then:

* kubelet (can be -2 minor version behind kube-apiserver)
* kube-proxy

Components same minor version as kube-apiserver


##### Upgrade Node procedure


1. Safely evicts all pods from node

```
kubectl drain
```

Mark node as SchedulingDisabled

```
kubectl cordon
```

2. Do the upgrade procedure
...

3. Unmark node as SchedulingDisabled


```
kubectl uncordon
```


###### Notice

* pod `gracePeriod` / Terminating state
* pod `Lifecycle` Events
* `PodDisruptionBudget`
