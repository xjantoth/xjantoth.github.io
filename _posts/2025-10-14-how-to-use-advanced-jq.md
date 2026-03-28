---
title: "How to use jq as a professional"
date: 2024-02-21T15:00:30+0100
lastmod: 2024-02-21T15:00:30+0100
draft: false
description: "Advanced jq example that parses a Terraform Cloud API response to extract run details including branch, commit info, and status timestamps."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['jq', 'bash']
categories: ["Linux"]
---

This advanced `jq` expression parses the Terraform Cloud API response (JSON:API format) to extract run metadata. It cross-references the `included` objects by ID to resolve nested relationships between runs, configuration versions, and ingress attributes, pulling out branch names, commit details, and status timestamps into a flat structure.

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
