---
title: "Force delete pods"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "Force delete pods"

tags: ['kubernetes', 'delete', 'pod']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
kubectl delete pod drillcluster1-drillbit-0 zk-0 --grace-period=0 --force

 kubectl patch pod drillcluster1-drillbit-0 zk-0  -p '{"metadata":{"finalizers":null}}'
```
