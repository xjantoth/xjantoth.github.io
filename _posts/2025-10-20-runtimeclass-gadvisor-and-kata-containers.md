---
title: "RuntimeClass GAdvisor and  Kata containers"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "RuntimeClass GAdvisor and  Kata containers"

tags: ['runtimeclass', 'gadvisor', 'kata', 'containers']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Prepare runtimeClass yaml specification''

```
k get runtimeclasses.node.k8s.io -A
NAME              HANDLER        AGE
gvisor            runsc          2m58s
kata-containers   kata-runtime   2m57s

vim runtimeclass.yaml
...
apiVersion: node.k8s.io/v1  # RuntimeClass is defined in the node.k8s.io API group
kind: RuntimeClass
metadata:
  name: secure-runtime # The name the RuntimeClass will be referenced by
  # RuntimeClass is a non-namespaced resource
handler: runsc  # The name of the corresponding CRI configuration
:wq!
```
**Create a custom runtimeClass by using kubectl command''

```
# apply this file
k create -f  runtimeclass.yaml
runtimeclass.node.k8s.io/secure-runtime created

# check a newly created runtimeClass
k get runtimeclasses.node.k8s.io -A
NAME              HANDLER        AGE
gvisor            runsc          7m25s
kata-containers   kata-runtime   7m24s
secure-runtime    runsc          2m48s
```
**Create a pod using secure-runtime runtimeClass''

```yaml
# create a pod using secure-runtime runtimeclass
cat simple-webapp-1.yaml
apiVersion: v1
kind: Pod
metadata:
    name: simple-webapp-1
    labels:
        name: simple-webapp
spec:
    runtimeClassName: secure-runtime
    containers:
        -
            name: simple-webapp
            image: kodekloud/webapp-delayed-start
            ports:
                -
                    containerPort: 8080
```
