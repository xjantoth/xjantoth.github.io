---
title: "Deployments"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Kubernetes Deployments: how to update container images and view rollout history using kubectl."

tags: ['deployments']
categories: ["Kubernetes"]
---

The `kubectl set image` command updates the container image for a deployment. Using `--dry-run=server` lets you validate the change without applying it, and `--record` annotates the rollout history with the command that triggered each revision. You can then inspect the revision history with `kubectl rollout history`.

```bash
kubectl set image deployment/frontend *=kodekloud/webapp-color:v2 --dry-run=server --record

controlplane $ kubectl  rollout history deployment frontend
deployment.apps/frontend
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/frontend *=kodekloud/webapp-color:v2 --record=true

```
