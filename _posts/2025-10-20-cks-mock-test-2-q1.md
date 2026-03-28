---
title: "CKS Mock test 2 - Q1"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "CKS mock test 2, question 1: Create a NetworkPolicy to restrict access to a redis-backend pod using namespace and pod label selectors."

tags: ['cks', 'mock', 'q1']
categories: ["Kubernetes"]
---

**1. A pod called redis-backend has been created in the prod-x12cs namespace. It has been exposed as a service of type ClusterIP. Using a network policy called allow-redis-access, lock down access to this pod only to the following:
1. Any pod in the same namespace with the label backend=prod-x12cs.
2. All pods in the prod-yx13cs namespace.
All other incoming connections should be blocked.

Use the existing labels when creating the network policy.

The following NetworkPolicy allows ingress traffic to the redis-backend pod on port 6379 from pods matching the `backend: prod-x12cs` label in the same namespace, as well as from all pods in namespaces labeled `access: redis`.

```yaml
cat 1.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-redis-access
  namespace: prod-x12cs
spec:
  podSelector:
    matchLabels:
      run: redis-backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          access: redis
    - podSelector:
        matchLabels:
          backend: prod-x12cs
    ports:
    - protocol: TCP
      port: 6379
```

**Test NetworkPolicy**

Verify the network policy by attempting to connect from a pod in the allowed namespace. A successful connection (even with an empty reply) confirms that the policy permits the traffic.

```bash
k exec -it -n prod-yx13cs nginx -- curl 10.44.0.3:6379
curl: (52) Empty reply from server
command terminated with exit code 52
```
