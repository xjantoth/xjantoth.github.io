---
title: "MOCK EXAM 2 CKA"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "MOCK EXAM 2 CKA — practical walkthrough with examples."

tags: ['mock', 'exam', 'cka']
categories: ["DevOps"]
---

```go
kubectl  run dns -it --image=busybox:1.28 --restart Never  -- nslookup resolver-service.default.svc > CKA/nginx.svc

kubectl  run dns -it --image=busybox:1.28 --restart Never  -- nslookup 10-244-1-8.default.pod > CKA/nginx.pod
```
