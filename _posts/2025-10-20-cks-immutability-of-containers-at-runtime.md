---
title: "CKS Immutability of containers at runtime"
date: 2022-06-09T10:34:54+0200
lastmod: 2022-06-09T10:34:54+0200
draft: false
description: "CKS Immutability of containers at runtime"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'immutability', 'of', 'containers', 'at', 'runtime']
---

* advanced deployment methods
* easy rollback
* more reliability
* better security (on container level)

![Image](/assets/images/blog/im-1.png)
![Image](/assets/images/blog/im-2.png)
![Image](/assets/images/blog/im-3.png)
![Image](/assets/images/blog/im-4.png)

##### Interesting example of how ''startupProbe'' can be used to make container a bit more secure

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

Generate pod receip


```
k run pod-ro -n sun --image=busybox:1.32.0 --dry-run=client -oyaml --command  -- sh -c 'sleep 1d' > pod.yaml
```

```
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
