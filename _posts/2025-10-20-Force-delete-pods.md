---
title: "Force delete pods"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Kubernetes: Force delete pods — configuration and practical examples."

tags: ['kubernetes', 'pod']
categories: ["Kubernetes"]
---

```
kubectl delete pod drillcluster1-drillbit-0 zk-0 --grace-period=0 --force

 kubectl patch pod drillcluster1-drillbit-0 zk-0  -p '{"metadata":{"finalizers":null}}'
```
