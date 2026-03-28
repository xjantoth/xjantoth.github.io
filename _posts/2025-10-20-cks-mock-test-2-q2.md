---
title: "CKS Mock test 2 - Q2"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "CKS mock test 2, question 2: Create a NetworkPolicy to allow only app1 and app2 pods to access the redis-backend, blocking app3."

tags: ['cks', 'mock', 'q2']
categories: ["Kubernetes"]
---

**A few pods have been deployed in the apps-xyz namespace. There is a pod called redis-backend which serves as the backend for the apps app1 and app2. The pod called app3 on the other hand, does not need access to this redis-backend pod. Create a network policy called allow-app1-app2 that will only allow incoming traffic from app1 and app2 to the redis-pod.


Make sure that all the available labels are used correctly to target the correct pods. Do not make any other changes to these objects.

This NetworkPolicy targets the redis-backend pod (matching labels `tier: backend` and `role: db`) and allows ingress only from pods labeled `name: app1` or `name: app2`, both with `tier: frontend`, on TCP port 6379.

```yaml
cat 2.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-app1-app2
  namespace: apps-xyz
spec:
  podSelector:
    matchLabels:
      tier: backend
      role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: app1
          tier: frontend
    - podSelector:
        matchLabels:
          name: app2
          tier: frontend
    ports:
    - protocol: TCP
      port: 6379
```

**Test**

Verify the policy works by testing connectivity from each pod. App3 should time out, while app1 and app2 should successfully connect to the redis-backend on port 6379.

```bash
controlplane $ k exec -it -n apps-xyz app3  -- nc -vz -w1 10.44.0.5:6379
nc: 10.44.0.5:6379 (10.44.0.5:6379): Operation timed out
command terminated with exit code 1

controlplane $ k exec -it -n apps-xyz app2  -- nc -vz -w1 10.44.0.5:6379
10.44.0.5:6379 (10.44.0.5:6379) open


controlplane $ k exec -it -n apps-xyz app1  -- nc -vz -w1 10.44.0.5:6379
10.44.0.5:6379 (10.44.0.5:6379) open
```
