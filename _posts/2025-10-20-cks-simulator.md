---
title: "CKS simulator"
date: 2022-06-13T14:32:22+0200
lastmod: 2022-06-13T14:32:22+0200
draft: false
description: "CKS exam topic: simulator — concepts, configuration, and practice exercises."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'simulator']
categories: ["Kubernetes"]
---


```
k get pods -A -o jsonpath='{range .items[*]}{.spec.nodeName}{"\t\t\t\t"}{.spec.containers[*].image}{"\t"}{"\n"}{end}'  | sort | grep cluster1-worker1
```
