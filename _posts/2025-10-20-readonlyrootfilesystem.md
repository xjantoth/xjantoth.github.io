---
title: "ReadOnlyRootFilesystem"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "ReadOnlyRootFilesystem — practical walkthrough with examples."

tags: ['readonlyrootfilesystem']
categories: ["DevOps"]
---

First, delete any existing pod and recreate it from the manifest. The `--grace-period 0 --force` flags ensure immediate deletion.

```bash
root@cks-master:~# k delete  po immutable --grace-period 0 --force

root@cks-master:~# k create  -f immutable.yaml
```

The pod spec below sets `readOnlyRootFilesystem: true` to prevent any writes to the container filesystem. An `emptyDir` volume is mounted at the log directory so Apache can still write its logs.

```yaml
cat immutable.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: immutable
  name: immutable
spec:
  containers:
  - image: httpd
    name: immutable
    securityContext:
      readOnlyRootFilesystem: true
    volumeMounts:
    - name: pid
      mountPath: "/usr/local/apache2/logs/"
  volumes:
  - name: pid
    emptyDir: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```
