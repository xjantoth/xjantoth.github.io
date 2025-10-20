---
title: "Remove taint"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "assets/images/blog/kubernetes-1.jpg"
description: "Remove taint"

tags: ["kubernetes", "remove", "taint"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
kubectl taint node archlinux node.kubernetes.io/disk-pressure:NoSchedule-
```
