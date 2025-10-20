---
title: How to detect duplicates using jq
date: 2024-05-10T21:11:50+0200
lastmod: 2024-05-10T21:11:50+0200
draft: false
description: How to detect duplicates using jq
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags:
  - bash
  - devopsinuse
  - jq
---

How to detect duplicates using jq


```bash
yq -o=json eval  data/aaa/bbb.yaml | jq '.ldap.ldap.members  | group_by(.) | map(select(length>1) | .[0])'

```

## Links:

202405102105
