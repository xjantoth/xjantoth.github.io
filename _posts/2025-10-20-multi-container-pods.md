---
title: "Multi-Container Pods"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Multi-Container Pods — practical walkthrough with examples."

tags: ['pods']
categories: ["Kubernetes"]
---

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: app
  name: app
  namespace: elastic-stack
spec:
  containers:
  - image: kodekloud/event-simulator
    name: app
    volumeMounts:
    - mountPath: /log
      name: log-volume
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-7lfvx
      readOnly: true
  - image: kodekloud/filebeat-configured
    name: sidecar
    volumeMounts:
    - mountPath: /var/log/event-simulator/
      name: log-volume
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-7lfvx
      readOnly: true
  serviceAccount: default
  serviceAccountName: default
  volumes:
  - hostPath:
      path: /var/log/webapp
      type: DirectoryOrCreate
    name: log-volume
  - name: default-token-7lfvx
    secret:
      defaultMode: 420
      secretName: default-token-7lfvx
```
