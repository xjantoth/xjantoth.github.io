---
title: How to deduplicate elements using jq
date: 2024-06-05T14:54:14+0200
lastmod: 2024-06-05T14:54:14+0200
description: "Practical guide: how to deduplicate elements using jq."
image: "https://miro.medium.com/v2/0*sV8pi5txXJiFOJfJ.png"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'jq']
categories: ["Linux"]
---

## Input file

The following YAML file contains a list with duplicate entries that we want to identify.

```yaml
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

Use `yq` to convert the YAML to JSON, then pipe it to `jq` with `group_by(.)` to group identical elements together. The `select(length>1)` filter keeps only groups with duplicates, and `.[0]` picks one representative from each group.

```bash
[arch:devopsinuse main()] yq -o=json eval  /tmp/deduplicate.yaml | jq '.some.awesome.members  | group_by(.) | map(select(length>1) | .[0])'

[
  "green"
]
```


