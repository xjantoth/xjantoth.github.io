---
title: How to detect duplicates using jq
date: 2024-05-10T21:11:50+0200
lastmod: 2024-05-10T21:11:50+0200
draft: false
description: "Practical guide: how to detect duplicates using jq."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'jq']
categories: ["Linux"]
---

How to detect duplicates using jq


```bash
yq -o=json eval  data/aaa/bbb.yaml | jq '.ldap.ldap.members  | group_by(.) | map(select(length>1) | .[0])'

```

## Links:

202405102105
