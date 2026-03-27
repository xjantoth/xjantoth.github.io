---
title: "ResourceQuota"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "ResourceQuota — practical walkthrough with examples."

tags: ['resourcequota']
categories: ["DevOps"]
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
