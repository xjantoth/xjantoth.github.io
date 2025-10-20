---
title: "Drain node from K3S"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "Drain node from K3S"

tags: ["kubernetes", "drain", "node", "k3s"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##  Deleted node from K8s

```
kubectl drain  k3s-ubuntu-18-04 --ignore-daemonsets --delete-local-data
kubectl delete node  k3s-ubuntu-18-04
```
