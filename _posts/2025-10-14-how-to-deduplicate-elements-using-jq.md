---
title: How to deduplicate elements using jq
date: 2024-06-05T14:54:14+0200
lastmod: 2024-06-05T14:54:14+0200
description: How to deduplicate elements using jq
image: https://miro.medium.com/v2/0*sV8pi5txXJiFOJfJ.png
author: "Jan Toth"
tags: ["bash", "devopsinuse", "jq"]
---

## Input file

```bash

some:
  awesome:
    members:
      - green
      - yellow
      - blue
      - red
      - green
```

## Deduplication

```bash
[arch:devopsinuse main()] yq -o=json eval  /tmp/deduplicate.yaml | jq '.some.awesome.members  | group_by(.) | map(select(length>1) | .[0])'

[
  "green"
]
```


