---
title: "CKS upgrade kubernetes"
date: 2022-04-26T10:53:27+0200
lastmod: 2022-04-26T10:53:27+0200
draft: false
description: "Step-by-step procedure for upgrading Kubernetes master and worker nodes, including draining, cordoning, and version management."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'upgrade', 'kubernetes']
categories: ["Kubernetes"]
---

Kubernetes follows semantic versioning with major, minor, and patch components.

```text
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


1. Safely evict all pods from the node. This command also marks the node as unschedulable (cordoned).

```bash
kubectl drain
```

Mark the node as SchedulingDisabled without evicting pods.

```bash
kubectl cordon
```

2. Do the upgrade procedure
...

3. Unmark the node as SchedulingDisabled, allowing pods to be scheduled on it again.

```bash
kubectl uncordon
```


###### Notice

* pod `gracePeriod` / Terminating state
* pod `Lifecycle` Events
* `PodDisruptionBudget`
