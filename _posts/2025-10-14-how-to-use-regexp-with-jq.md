---
title: How to use regexp with jq
date: 2024-06-17T13:54:17+0200
lastmod: 2024-06-17T13:54:17+0200
draft: false
description: "How to use regexp within jq when selecting documents."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'jq', 'regexp']
categories: ["Linux"]
---

How to use regexp within `jq` when selecting documents.

The `test()` function in `jq` matches a string against a regular expression. Combined with `--arg` to pass shell variables into `jq`, this lets you dynamically filter GCP project lists by name patterns. This is useful when you need to find projects matching a specific naming convention.

```bash
PROJECT_NAMES="one|two|there"
REGEXP_SOL_PROJ="^prefix-${ENVIRONMENT}-(${PROJECT_NAMES}).*"
REGION="europe-west3"

HSM_PROJ=$(gcloud projects --format=json list | jq -r --arg RGEXP "^eaut-${ENVIRONMENT}-hsm-dap-kernel.*$" '.[] | select(.projectId|test($RGEXP)) | .projectId')

```


