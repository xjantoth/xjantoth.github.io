---
title: "CKS Immutability of containers at runtime"
date: 2022-06-09T10:34:54+0200
lastmod: 2022-06-09T10:34:54+0200
draft: false
description: "How to enforce container immutability at runtime in Kubernetes using startupProbe, readOnlyRootFilesystem, and emptyDir volumes."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'immutability', 'containers', 'runtime']
categories: ["Kubernetes"]
---

* advanced deployment methods
* easy rollback
* more reliability
* better security (on container level)

![Image](/assets/images/blog/im-1.png)
![Image](/assets/images/blog/im-2.png)
![Image](/assets/images/blog/im-3.png)
![Image](/assets/images/blog/im-4.png)

##### Interesting example of how startupProbe can be used to make a container a bit more secure

```yaml
root@cks-master:~# cat immutable.yaml
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
    resources: {}
    startupProbe:
      exec:
        command:
        - rm
        - /bin/bash
      initialDelaySeconds: 1
      periodSeconds: 5
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```


##### ReadOnlyRootFilesystem example

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

##### If you come from Docker world

![Image](/assets/images/blog/im-5.png)



##### Task

Generate a pod recipe with a read-only root filesystem. This command creates a dry-run YAML manifest for a busybox pod that sleeps for one day.

```bash
k run pod-ro -n sun --image=busybox:1.32.0 --dry-run=client -oyaml --command  -- sh -c 'sleep 1d' > pod.yaml
```

Then add the `readOnlyRootFilesystem` security context to the generated manifest.

```yaml
controlplane $ cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod-ro
  name: pod-ro
  namespace: sun
spec:
  containers:
  - command:
    - sh
    - -c
    - sleep 1d
    image: busybox:1.32.0
    name: pod-ro
    resources: {}
    securityContext:
      readOnlyRootFilesystem: true
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```
