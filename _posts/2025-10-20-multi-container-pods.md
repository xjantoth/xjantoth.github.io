---
title: "Multi-Container Pods"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Multi-Container Pods"

tags: ['pods']
categories: ["tiddlywiki"]

hiddenFromSearch: false
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
