---
title: "Node Affinity"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Kubernetes node affinity example that schedules pods only on nodes matching a specific label using requiredDuringSchedulingIgnoredDuringExecution."

tags: ['node', 'affinity']
categories: ["DevOps"]
---

##  Match node label

This deployment snippet uses `nodeAffinity` with `requiredDuringSchedulingIgnoredDuringExecution` to ensure pods are only scheduled on nodes that have the label `color=blue`. This is useful when you need to target specific hardware or node pools.

```yaml
     app: blue
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: blue
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: color
                operator: In
                values:
                - blue
      containers:
      - image: nginx
        imagePullPolicy: Always
        name: nginx
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
```
