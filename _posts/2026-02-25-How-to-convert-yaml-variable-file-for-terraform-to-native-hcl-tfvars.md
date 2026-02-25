---
title: "How to convert yaml variable file for terraform to native hcl tfvars"
date: 2026-02-25T14:15:53+01:00
lastmod: 2026-02-25T14:15:53+01:00
draft: false
description: "How to convert yaml variable file for terraform to native hcl tfvars"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: []
---

If there is ever a need to convert yaml variable file for terraform to native hcl tfvars, one can 
use this command.

```bash
brew install json2hcl
cat data/prod/root.yaml| yq -ojson | jq .azure_secret_engines | json2hcl
```
