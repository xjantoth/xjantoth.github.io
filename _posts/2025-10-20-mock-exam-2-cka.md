---
title: "Mock Exam 2 - CKA"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "CKA Mock Exam 2 solutions covering DNS resolution testing for services and pods using nslookup from a busybox container."

tags: ['mock', 'exam', 'cka']
categories: ["DevOps"]
---

These commands run a temporary busybox pod to perform DNS lookups within the cluster. The first command resolves a Kubernetes service by its FQDN, and the second resolves a pod by its dashed-IP DNS record. Both outputs are saved to files for verification.

```bash
kubectl  run dns -it --image=busybox:1.28 --restart Never  -- nslookup resolver-service.default.svc > CKA/nginx.svc

kubectl  run dns -it --image=busybox:1.28 --restart Never  -- nslookup 10-244-1-8.default.pod > CKA/nginx.pod
```
