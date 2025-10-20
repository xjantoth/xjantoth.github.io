---
title: "Create Pod on the fly"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "Create Pod on the fly"

tags: ["kubernetes", "pod", "kubectl"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
kubectl run -i --tty busybox --image=gcr.io/kubernetes-e2e-test-images/dnsutils:1.3 --restart=Never -- sh
kubectl run -i --tty busybox --image=busybox --restart=Never -- sh
```
