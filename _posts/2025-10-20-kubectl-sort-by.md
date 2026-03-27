---
title: "kubectl sort by"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"

description: "Kubernetes: kubectl sort by — configuration and practical examples."

tags: ['kubernetes', 'by']
categories: ["Kubernetes"]
---

```
kubectl get pods -o wide -n prod --sort-by=.spec.nodeName
```
