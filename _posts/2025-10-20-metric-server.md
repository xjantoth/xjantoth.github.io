---
title: "Metrics Server"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Install the Kubernetes Metrics Server with the kubelet-insecure-tls flag for lab and development environments."

tags: ['metric', 'server']
categories: ["DevOps"]
---

These commands download the Metrics Server manifest, patch it to add the `--kubelet-insecure-tls` flag (required in self-signed or lab environments where kubelet certificates are not trusted), and then deploy it to the cluster.

```bash
wget  https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
sed -iE 's/^(.*--kubelet-use-node-status-port)/\1 \n        - --kubelet-insecure-tls/' components.yaml
kubectl create -f components.yaml
```
