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

This command detects duplicate entries in a YAML array using `yq` and `jq`. It converts the YAML to JSON, groups array elements, and filters for groups with more than one member. This is useful for catching accidental duplicates in configuration files such as LDAP group memberships.

```bash
yq -o=json eval  data/aaa/bbb.yaml | jq '.ldap.ldap.members  | group_by(.) | map(select(length>1) | .[0])'

```

