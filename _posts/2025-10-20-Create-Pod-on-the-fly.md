---
title: "Create Pod on the fly"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Kubernetes: Create Pod on the fly — configuration and practical examples."

tags: ['kubernetes', 'pod', 'kubectl']
categories: ["Kubernetes"]
---

These commands create temporary, interactive pods directly from the command line without writing YAML manifests. The first variant uses a DNS utilities image, which is useful for debugging DNS resolution inside the cluster. The second uses a minimal BusyBox image for general-purpose troubleshooting.

```bash
kubectl run -i --tty busybox --image=gcr.io/kubernetes-e2e-test-images/dnsutils:1.3 --restart=Never -- sh
kubectl run -i --tty busybox --image=busybox --restart=Never -- sh
```
