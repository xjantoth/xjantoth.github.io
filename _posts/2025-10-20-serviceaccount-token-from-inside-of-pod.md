---
title: "ServiceAccount token from inside of pod"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "ServiceAccount token from inside of pod — practical walkthrough with examples."

tags: ['serviceaccount', 'token', 'inside', 'pod']
categories: ["Kubernetes"]
---

```perl
curl https://kubernetes -k -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceaccount/token)"
```
