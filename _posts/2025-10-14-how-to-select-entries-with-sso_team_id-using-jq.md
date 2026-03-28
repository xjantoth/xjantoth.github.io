---
title: How to select entries with sso_team_id using jq
date: 2024-06-05T12:58:07+0200
lastmod: 2024-06-05T12:58:07+0200
draft: false
description: "Practical guide: how to select entries with sso_team_id using jq."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'jq']
categories: ["Linux"]
---

###### Goal

How to choose only records that have sso_team_id key defined?


###### Input file to process with `jq` and `yq`

The following YAML file contains identity definitions where only some entries have the `sso_team_id` key.

```yaml

identities:
  team1:
    oidc: oidc
    type: external
    metadata:
      version: 1
      description: cloud team
    policies:
      - aaa-admin
    sso_team_id: VLT-TEAM_1

  team2:
    oidc: oidc
    type: external
    metadata:
      version: 1
      description: cloud team
    policies:
      - aaa-admin

  team3:
    oidc: oidc
    type: external
    metadata:
      version: 1
      description: cloud team
    policies:
      - aaa-admin
    sso_team_id: VLT-TEAM_3

```

###### Processing

This `jq` expression iterates over all keys in the `identities` object, builds key-value pairs of identity name to `sso_team_id`, merges them into a single object, and filters out entries where the value is null.

```bash
yq -o=json eval /tmp/aaa.yaml | jq '.identities | [keys[] as $k | {($k): .[$k].sso_team_id}]  | add | with_entries(select(.value |.!=null))'

{
  "team1": "VLT-TEAM_1",
  "team3": "VLT-TEAM_3"
}
```

