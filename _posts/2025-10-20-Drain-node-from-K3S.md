---
title: "Drain node from K3S"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "How to safely drain and delete a node from a K3S Kubernetes cluster using kubectl."

tags: ['kubernetes', 'drain', 'node', 'k3s']
categories: ["Kubernetes"]
---

## Remove a node from K3S

To safely remove a node, first drain it to evict all running pods (ignoring DaemonSets and deleting local data), then delete the node object from the cluster. This ensures workloads are rescheduled to other nodes before the node is removed.

```bash
kubectl drain  k3s-ubuntu-18-04 --ignore-daemonsets --delete-local-data
kubectl delete node  k3s-ubuntu-18-04
```
