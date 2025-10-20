---
title: "ResourceQuota"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "ResourceQuota"

tags: ['resourcequota']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
kubectl create quota myrq --hard=cpu=1,memory=1G,pods=2 -o yaml --dry-run=client
apiVersion: v1
kind: ResourceQuota
metadata:
  creationTimestamp: null
  name: myrq
spec:
  hard:
    cpu: "1"
    memory: 1G
    pods: "2"
status: {}
```
