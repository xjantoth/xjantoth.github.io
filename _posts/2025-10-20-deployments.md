---
title: "Deployments"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Deployments"

tags: ['deployments']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
kubectl set image deployment/frontend *=kodekloud/webapp-color:v2 --dry-run=server --record

controlplane $ kubectl  rollout history deployment frontend
deployment.apps/frontend
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/frontend *=kodekloud/webapp-color:v2 --record=true

```
