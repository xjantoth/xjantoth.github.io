---
title: "CKS simulator"
date: 2022-06-13T14:32:22+0200
lastmod: 2022-06-13T14:32:22+0200
draft: false
description: "CKS simulator"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'simulator']
---


```
k get pods -A -o jsonpath='{range .items[*]}{.spec.nodeName}{"\t\t\t\t"}{.spec.containers[*].image}{"\t"}{"\n"}{end}'  | sort | grep cluster1-worker1
```
