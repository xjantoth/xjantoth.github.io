---
title: "ServiceAccount token from inside of pod"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "How to use the mounted ServiceAccount token from inside a Kubernetes pod to authenticate against the Kubernetes API."

tags: ['serviceaccount', 'token', 'inside', 'pod']
categories: ["Kubernetes"]
---

Every pod in Kubernetes automatically gets a ServiceAccount token mounted at `/run/secrets/kubernetes.io/serviceaccount/token`. You can use this token to authenticate API requests from inside the pod. The following curl command calls the Kubernetes API using the bearer token.

```bash
curl https://kubernetes -k -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceaccount/token)"
```
