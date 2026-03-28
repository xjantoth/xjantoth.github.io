---
title: "How to make sure that pod will be scheduled only on Control Plane"
date: 2026-01-07T22:19:07:+0100
lastmod: 2026-01-07T22:19:07:+0100
draft: false
description: "Practical guide: how to make sure that pod will be scheduled only on Control Plane."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: []
categories: ["Kubernetes"]
---

To ensure a pod runs exclusively on the control plane node, you need two things: a toleration for the control plane taint (so the scheduler does not reject it) and a node affinity rule that requires the `node-role.kubernetes.io/control-plane` label to be present. The combination guarantees the pod is both allowed and required to land on the control plane.

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
