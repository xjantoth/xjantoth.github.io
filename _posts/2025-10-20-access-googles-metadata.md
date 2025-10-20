---
title: "Access Google's metadata"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Access Google's metadata"

tags: ['access', "google's", 'metadata']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

Access Google's metadata

```perl
curl http://metadata.google.internal/computeMetadata/v1/instance/id -H "Metadata-Flavor: Google"
```
