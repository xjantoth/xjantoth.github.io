---
title: "How to make sure that pod will be scheduled only on controlplaane"
date: 2026-01-07T22:19:07:+0100
lastmod: 2026-01-07T22:19:07:+0100
draft: false
description: "How to make sure that pod will be scheduled only on controlplaane"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: []
---


```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: pod1
  name: pod1
spec:
  tolerations:
    - key: "node-role.kubernetes.io/control-plane"
      effect: "NoSchedule"
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: "node-role.kubernetes.io/control-plane"
            operator: Exists
  containers:
  - image: httpd:2-alpine
    name: pod1-container
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```
