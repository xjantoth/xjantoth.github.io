---
title: "CKS simulator"
date: 2022-06-13T14:32:22+0200
lastmod: 2022-06-13T14:32:22+0200
draft: false
description: "Useful kubectl commands for the CKS simulator exam environment, including listing pods with their node assignments and container images."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'simulator']
categories: ["Kubernetes"]
---

The following command lists all pods across all namespaces, showing which node each pod is scheduled on and what container images it uses. The output is sorted and filtered to show only pods running on `cluster1-worker1`.

```bash
k get pods -A -o jsonpath='{range .items[*]}{.spec.nodeName}{"\t\t\t\t"}{.spec.containers[*].image}{"\t"}{"\n"}{end}'  | sort | grep cluster1-worker1
```
