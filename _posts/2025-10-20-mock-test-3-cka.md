---
title: "Mock Test 3 - CKA"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "CKA Mock Test 3 solutions covering multi-container pods, security contexts, network policies, and pod tolerations."

tags: ['mock', 'cka']
categories: ["DevOps"]
---

Below are the YAML manifests for CKA Mock Test 3. They include multi-container pods with environment variables, pods with non-root security contexts, network policies for ingress filtering, and pods with tolerations for tainted nodes.

```yaml
controlplane $ for i in $(ls *.yaml); do echo -e "$i\n\n"; cat $i; done
03.yaml


apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: multi-pod
  name: multi-pod
spec:
  containers:
  - image: nginx
    name: alpha
    env:
    - name: name
      value: "alpha"
  - image: busybox
    name: beta
    env:
    - name: name
      value: "beta"
    command: ["sh", "-c", "sleep 4800"]


    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
04.yaml


apiVersion: v1
kind: Pod
metadata:
  name: non-root-pod
spec:
  securityContext:
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: non-root-pod
    image: redis:alpine
05.yaml


apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: np-test-1
  policyTypes:
  - Ingress
  ingress:
  - from:
    ports:
    - protocol: TCP
      port: 80


606.yaml


apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: prod-redis
  name: prod-redis
spec:
  containers:
  - image: redis:alpine
    name: prod-redis
    resources: {}
  tolerations:
  - key: "env_type"
    operator: "Equal"
    value: "production"
    effect: "NoSchedule"
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```
