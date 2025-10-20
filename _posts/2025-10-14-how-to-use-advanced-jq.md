---
title: "How to use jq as professional"
date: 2024-02-21T15:00:30+0100
lastmod: 2024-02-21T15:00:30+0100
draft: false
description: "How to use jq as PRO"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['jq', 'bash']
---

```bash
curl -s \
      --header "Authorization: Bearer $TOKEN" \
      --header "Content-Type: application/vnd.api+json" \
      --request GET ${URL}  | jq -r '(.included |
  map({(.id): .}) | add) as $inc |
  .data[] | {"run-id": .id} +
  ($inc[$inc[.relationships."configuration-version".data.id].relationships."ingress-attributes".data.id].attributes |
  {
    branch,
    "commit-message",
    "sender-username",
    "clone-url",
    "commit-url",
    "compare-url",
    identifier
  }) +
  (.attributes."status-timestamps"|
    {
      "applied-at",
      "planned-at",
      "queuing-at",
      "applying-at",
      "planning-at",
      "confirmed-at",
      "plan-queued-at",
      "apply-queued-at",
      "queuing-apply-at",
      "plan-queueable-at",

    }
  ) + (.attributes |
    {
      "trigger-reason"

    }
  )
  '

```
