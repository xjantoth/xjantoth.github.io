---
title: "Drain node from K3S"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Deleted node from K8s."

tags: ['kubernetes', 'drain', 'node', 'k3s']
categories: ["Kubernetes"]
---

##  Deleted node from K8s

```
kubectl drain  k3s-ubuntu-18-04 --ignore-daemonsets --delete-local-data
kubectl delete node  k3s-ubuntu-18-04
```
