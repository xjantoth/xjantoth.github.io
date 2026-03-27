---
title: "Deployments"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Deployments — practical walkthrough with examples."

tags: ['deployments']
categories: ["Kubernetes"]
---

```
kubectl set image deployment/frontend *=kodekloud/webapp-color:v2 --dry-run=server --record

controlplane $ kubectl  rollout history deployment frontend
deployment.apps/frontend
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/frontend *=kodekloud/webapp-color:v2 --record=true

```
