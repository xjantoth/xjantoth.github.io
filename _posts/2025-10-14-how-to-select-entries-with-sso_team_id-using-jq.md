---
title: How to select entries with sso_team_id using jq
date: 2024-06-05T12:58:07+0200
lastmod: 2024-06-05T12:58:07+0200
draft: false
description: How to select entries with sso_team_id using jq
image: "images/blog/linux-1.jpg"
author: "Jan Toth"
tags:
  - bash
  - devopsinuse
  - jq
---

###### Goal

How to choose only records that have sso_team_id key defined?


###### Input file to process with `jq` and `yq`.

```

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

```
yq -o=json eval /tmp/aaa.yaml | jq '.identities | [keys[] as $k | {($k): .[$k].sso_team_id}]  | add | with_entries(select(.value |.!=null))'

{
  "team1": "VLT-TEAM_1",
  "team3": "VLT-TEAM_3"
}
```

## Links:

202406051206
