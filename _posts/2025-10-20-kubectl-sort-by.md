---
title: "kubectl sort by"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"

description: "kubectl sort by"

tags: ['kubernetes', 'by']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
kubectl get pods -o wide -n prod --sort-by=.spec.nodeName
```
