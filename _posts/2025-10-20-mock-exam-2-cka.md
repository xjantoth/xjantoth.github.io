---
title: "MOCK EXAM 2 CKA"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "MOCK EXAM 2 CKA"

tags: ['mock', 'exam', 'cka']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
kubectl  run dns -it --image=busybox:1.28 --restart Never  -- nslookup resolver-service.default.svc > CKA/nginx.svc

kubectl  run dns -it --image=busybox:1.28 --restart Never  -- nslookup 10-244-1-8.default.pod > CKA/nginx.pod
```
