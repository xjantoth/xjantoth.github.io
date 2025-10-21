---
title: "ServiceAccount token from inside of pod"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "ServiceAccount token from inside of pod"

tags: ['serviceaccount', 'token', 'inside', 'pod']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```perl
curl https://kubernetes -k -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceaccount/token)"
```
