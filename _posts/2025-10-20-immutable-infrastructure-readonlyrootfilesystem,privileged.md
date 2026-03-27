---
title: "Immutable infrastructure (readOnlyRootFilesystem,privileged)"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Set ''UID'' and ''GID'' within ''securityContext'' for pod and verify results (''runAsUser'' and ''runAsGroup'')."

tags: ['immutable', 'infrastructure']
categories: ["DevOps"]
---

Set ''UID'' and ''GID'' within ''securityContext'' for pod and verify results (''runAsUser'' and ''runAsGroup'')

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: grimsby
  namespace: alpha
spec:
  containers:
  - command:
    - sh
    - -c
    - sleep 5h
    image: busybox
    imagePullPolicy: Always
    name: sec-ctx-demo
    securityContext:
      runAsUser: 1000
      runAsGroup: 3000
    volumeMounts:
    - mountPath: /data/demo
      name: demo-volume
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-4lmbt
      readOnly: true
...
  volumes:
  - emptyDir: {}
    name: demo-volume
  - name: default-token-4lmbt
    secret:
      defaultMode: 420
      secretName: default-token-4lmbt
```


Create Nginx pod with ''readOnlyRootFilesystem'' option and adjust necessary ''volumes'' (''/var/cache/nginx'', ''/var/run'')

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: solaris
  name: solaris
  namespace: alpha
spec:
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: solaris
    ports:
    - containerPort: 8080
      protocol: TCP
    resources: {}
    securityContext:
      privileged: false
      readOnlyRootFilesystem: true
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/cache/nginx
      name: nginx
    - mountPath: /var/run
      name: run
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-4lmbt
      readOnly: true
...
  volumes:
  - name: nginx
    emptyDir: {}
  - name: run
    emptyDir: {}

```

Run apache (httpd) with ''readOnlyRootFilesystem'' within security context as well as create temporary ''mountPath/volumeMounts''

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: triton
    namespace: alpha
  name: triton
  namespace: alpha
spec:
  containers:
  - image: httpd
    imagePullPolicy: Always
    name: triton
    resources: {}
    securityContext:
            readOnlyRootFilesystem: true
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-4lmbt
      readOnly: true
    - mountPath: /usr/local/apache2/logs
      name: apache
...
    tolerationSeconds: 300
  volumes:
  - name: apache
    emptyDir: {}

  - name: default-token-4lmbt
    secret:
      defaultMode: 420
      secretName: default-token-4lmbt
```
