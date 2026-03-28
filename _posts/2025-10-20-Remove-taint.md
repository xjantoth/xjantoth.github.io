---
title: "Remove taint"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Kubernetes: Remove taint — configuration and practical examples."

tags: ['kubernetes', 'taint']
categories: ["Kubernetes"]
---

Use `kubectl taint` with a trailing minus sign (`-`) to remove a specific taint from a node. This is useful when a node has been automatically tainted due to conditions like disk pressure and you want to allow scheduling again.

```bash
kubectl taint node archlinux node.kubernetes.io/disk-pressure:NoSchedule-
```
