---
title: How to use regexp with jq
date: 2024-06-17T13:54:17+0200
lastmod: 2024-06-17T13:54:17+0200
draft: false
description: How to use regexp with jq
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ["bash", "devopsinuse", "jq", "regexp"]
---

How to use regexp within `jq` when selecting documents

```bash
PROJECT_NAMES="one|two|there"
REGEXP_SOL_PROJ="^prefix-${ENVIRONMENT}-(${PROJECT_NAMES}).*"
REGION="europe-west3"

HSM_PROJ=$(gcloud projects --format=json list | jq -r --arg RGEXP "^eaut-${ENVIRONMENT}-hsm-dap-kernel.*$" '.[] | select(.projectId|test($RGEXP)) | .projectId')

```


