---
title: "RuntimeClass gVisor and Kata containers"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1605745341112-85968b19335b?w=800&h=420&fit=crop"
description: "How to configure Kubernetes RuntimeClass resources for gVisor and Kata containers to run workloads in sandboxed runtimes."

tags: ['runtimeclass', 'gadvisor', 'kata', 'containers']
categories: ["Docker"]
---

## Prepare runtimeClass YAML specification

First, list the existing RuntimeClasses available in the cluster to see what container runtimes are already configured. Then create a YAML file that defines a new RuntimeClass pointing to the desired handler.

```bash
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

## Create a custom runtimeClass by using kubectl command

Apply the YAML file to create the new RuntimeClass, then verify that it appears alongside the existing ones.

```bash
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

## Create a pod using secure-runtime runtimeClass

To use the new RuntimeClass, set the `runtimeClassName` field in the pod spec. This ensures the pod runs using the gVisor (runsc) sandboxed runtime instead of the default container runtime.

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
