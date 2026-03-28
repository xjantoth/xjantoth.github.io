---
title: "NetworkPolicy"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Kubernetes NetworkPolicy examples for controlling ingress and egress traffic to pods using label selectors and port rules."

tags: ['networkpolicy']
categories: ["DevOps"]
---

The first policy below allows incoming TCP traffic on port 80 to any pod with the label `run: np-test-1` from all sources. The second policy restricts egress from pods labeled `name: internal` to only MySQL (port 3306) and Payroll (port 8080) pods.

```yaml

# allow incoming traffic to pod "run: np-test-1" to port 80 from everywhere

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-to-nptest
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


cat  policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: internal-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      name: internal
  policyTypes:
  - Egress
  egress:
  # MySQL rule
  - to:
    - podSelector:
        matchLabels:
          name: mysql
    ports:
    - protocol: TCP
      port: 3306
  # Payroll rule
  - to:
    - podSelector:
        matchLabels:
          name: payroll
    ports:
    - protocol: TCP
      port: 8080
```
