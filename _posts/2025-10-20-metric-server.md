---
title: "Metric server"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Metric server"

tags: ['metric', 'server']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```c
wget  https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
sed -iE 's/^(.*--kubelet-use-node-status-port)/\1 \n        - --kubelet-insecure-tls/' components.yaml
kubectl create -f components.yaml
```
